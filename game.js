$(document).ready(
    function(){

       $("#svg-box img").each(
        function(){
            var $img = $(this)
            var imgClass = $img.attr("class")
            var imgUrl = $img.attr("src")
            $.get(imgUrl, function(data){
                var $svg = $(data).find("svg")
                $svg = $svg.removeAttr("xmlns:a")
                $svg.attr("class", imgClass)
                $img.replaceWith($svg)
            })
        }
       )

       $("svg-box").click(
        function(){
            $("circle").attr("fill", "GREEN")
        }
       )

    }
)