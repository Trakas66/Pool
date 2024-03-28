$(document).ready(
    function(){

        document.onmousemove = onMouseMove
        document.onclick = click

        let draw = false
        let drawStop = false
        var balls = []
        let colours = ["YELLOW", "BLUE", "RED", "PURPLE", "ORANGE", "GREEN", "BROWN"]
        var ball8 = 1
        var numSolids = 0
        var numStripes = 0
        var turn = 1
        var turnBalls = 0

        var p1Balls = 0
        var p2Balls = 0

        let p1name = $("#p1name").attr("data-name")
        let p2name = $("#p2name").attr("data-name")
        $("#p1name").text(p1name)
        $("#p2name").text(p2name)

        function createCue(){
            var cue = document.createElementNS("http://www.w3.org/2000/svg", 'line')
            let x = $("#cue-ball").attr('cx')
            let y = $("#cue-ball").attr('cy')
            cue.setAttributeNS(null, 'x1', x)
            cue.setAttributeNS(null, 'y1', y)
            cue.setAttributeNS(null, 'x2', x)
            cue.setAttributeNS(null, 'y2', y)
            cue.setAttributeNS(null, 'stroke', 'BLACK')
            cue.setAttributeNS(null, 'stroke-width', 10)
            cue.setAttributeNS(null, 'id', 'cue')
            return cue
        }

        loadSvg()

        function loadSvg(){

            $("#svg-box").load("table.svg", function(){
                setCueBall()
                populateArray()
                showTurn()
            })
            
        }
        

        function onMouseMove(event){
            if(draw){
                let ballX = parseFloat($("#cue-ball").attr('cx'))
                let ballY = parseFloat($("#cue-ball").attr('cy'))

                let bpageX = $("#cue-ball").offset().left
                let bpageY = $("#cue-ball").offset().top

                let spageX = $("#surface").offset().left

                var ratio = ballX / (bpageX - spageX)
                var x = (event.pageX - bpageX) * ratio + ballX
                var y = (event.pageY - bpageY) * ratio + ballY
                
                var length = Math.sqrt((x-ballX)*(x-ballX) + (y-ballY)*(y-ballY))
                if(length > 500){
                    var r = 500/length
                    x = ballX + (x- ballX) * r
                    y = ballY + (y-ballY) * r
                }

                $("#cue").attr("x2", x)
                $("#cue").attr("y2", y)
            }
        }
     
        function click(){
            if(draw){
                if(drawStop){
                    let x = $("#cue").attr("x2")
                    let y = $("#cue").attr("y2")
                    $("#cue").remove()
                    draw = false
                    drawStop = false
                    shoot(x, y)
                }else{
                    drawStop = true
                }
                
            }
        }

        function shoot(x, y){
            let ballX = $("#cue-ball").attr("cx")
            let ballY = $("#cue-ball").attr("cy")
            let id = $("#svg-box").attr("data-id")
            $.post("shoot", 
            {
                ballX:ballX,
                ballY:ballY,
                x:x,
                y:y,
                gameid:id
            }, showShot)

        }

        function showShot(data, status){
            var tables = data.split(":,:")
            tables.forEach(function(item, index){
                setTimeout(function(){
                    displayFrame(item)

                    if(index+1 == tables.length){
                        if($("#cue-ball").length == 0){
                            let id = $("#svg-box").attr("data-id")
                            $.post("placecue",
                            {
                                gameid:id
                            }, cueBallPlaced)
                        }
                        else{
                            setCueBall()
                        }
                        afterShot()
                    }

                }, 10 * (index + 1))
            })

        }

        function displayFrame(frame){
            $("#svg-box").html(frame)
        }

        function cueBallPlaced(data, status){
            displayFrame(data)
            setCueBall()
        }

        function setCueBall(){
            $("#cue-ball").click(
                function(){
                    if(!draw){
                        this.after(createCue())
                        draw = true
                    }
                    
                }
            )
        }

        function populateArray(){
            colours.forEach(function(item, index){
                balls.push($(`circle[fill="${item}"]`).length)
                if(balls[index] == 3){
                    numSolids += 1
                    numStripes += 1
                }else if(balls[index] == 2){
                    numStripes += 1
                }else if(balls[index] == 1){
                    numSolids += 1
                }
                
            })
            ball8 = $("circle[fill='BLACK'][r='28.5']").length
            console.log("NumSolids: " + numSolids + "\nNumStripes: " + numStripes)
        }

        function afterShot(){
            tempBalls = []
            solids = 0
            stripes = 0
            colours.forEach(function(item, index){
                tempBalls.push($(`circle[fill="${item}"]`).length)
                if(balls[index] - tempBalls[index] == 1){
                    numSolids -= 1
                    solids += 1
                }else if(balls[index] - tempBalls[index] == 2){
                    numStripes -= 1
                    stripes += 1
                }else if(balls[index] - tempBalls[index] == 3){
                    numSolids -= 1
                    numStripes -= 1
                    solids += 1
                    stripes += 1
                }
            })
            ball8 = $("circle[fill='BLACK'][r='28.5']").length

            console.log("NumSolids: " + numSolids + "\nNumStripes: " + numStripes)
            console.log("Solids: " + solids + "\nStripes: " + stripes)

            if(ball8 == 0){
                //game is over
                if(turnBalls == 0){
                    console.log("Game lost")
                }else if(turnBalls == 1){
                    if(numSolids == 0 && solids == 0){
                        console.log("Game won by solids")
                    }else{
                        console.log("Game lost by solids")
                    }
                }else{
                    if(numStripes == 0 && stripes == 0){
                        console.log("Game won by stripes")
                    }else{
                        console.log("Game lost by stripes")
                    }
                }
            }

            if(p1Balls == 0 && turn == 1 && numSolids != 7 && numStripes != 7){
                if(numSolids > numStripes){
                    p1Balls = 2
                    p2Balls = 1
                    turnBalls = 2
                }else{
                    p1Balls = 1
                    p2Balls = 2
                    turnBalls = 1
                }
                showTurn()
            }else if(p1Balls == 0 && turn == 2 && numSolids != 7 && numStripes != 7){
                if(numSolids > numStripes){
                    p1Balls = 1
                    p2Balls = 2
                    turnBalls = 2
                }else{
                    p1Balls = 2
                    p2Balls = 1
                    turnBalls = 1
                }
                showTurn()
            }else{

                if(turn == 1){
                    if(p1Balls == 1){
                        if(solids == 0){
                            changeTurn()
                        }
                    }else{
                        if(stripes == 0){
                            changeTurn()
                        }
                    }
                }else{
                    if(p2Balls == 1){
                        if(solids == 0){
                            changeTurn()
                        }
                    }else{
                        if(stripes == 0){
                            changeTurn()
                        }
                    }
                }

            }
            balls = tempBalls
            console.log("P1Balls: " + p1Balls + "\nP2Balls: " + p2Balls)
        }

        function changeTurn(){
            if(turn == 1){
                turn = 2
            }else{
                turn = 1
            }
            if(turnBalls == 1){
                turnBalls = 2
            }else if(turnBalls == 2){
                turnBalls = 1
            }

            showTurn()
            
        }

        function showTurn(){

            if(turn == 1){
                $("#turncontainer h3").text(p1name + "'s turn")
            }else{
                $("#turncontainer h3").text(p2name + "'s turn")
            }

            if(turnBalls == 1){
                $("#turncontainer p").text("Solids")
            }else if(turnBalls == 2){
                $("#turncontainer p").text("Stripes")
            }

        }

    }
)