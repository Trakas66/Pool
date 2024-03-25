$(document).ready(
    function(){

        document.onmousemove = onMouseMove
        document.onclick = click

        let draw = false
        let drawStop = false

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
                $("#cue-ball").click(
                    function(){
                        if(!draw){
                            this.after(createCue())
                            draw = true
                        }
                        
                    }
                )
            })
        }
        

        function onMouseMove(event){
            if(draw){
                let ballX = $("#cue-ball").attr('cx')
                let ballY = $("#cue-ball").attr('cy')

                let bpageX = $("#cue-ball").offset().left
                let bpageY = $("#cue-ball").offset().top

                let spageX = $("#surface").offset().left

                var ratio = ballX / (bpageX - spageX)
                var x = (event.pageX - bpageX) * ratio + +ballX
                var y = (event.pageY - bpageY) * ratio + +ballY

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
            loadSvg()
        }

    }
)