function getAnswersAndchange(keyword){

    $.post("/getanswer",{keyword:keyword,type:'zhidao'},function(data,status){document.getElementById('answer').innerHTML=data;})
}
// function changeAnswer(answer){
//
//     alert(answer);
// }
$(document).ready(function() {
    $('button#start').click(function () {
        var keyword = $('input#keyword').val();
        getAnswersAndchange(keyword)
    })
});