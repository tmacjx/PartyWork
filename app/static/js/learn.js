/**
 * Created by tmackan on 2017/5/22.
 */


$(document).ready(function () {

    get_important_file_video();


    get_important_file_text();


    get_theory_video();

    get_theory_text();


    get_paper_video();

    get_paper_text();


});


function show_important_file_video(data){

    // todo 新增页面元素
    // <video src="movie.ogg" controls="controls">
    // </video>

    // var video = ""


    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径 用html video标签

        console.log(data[i].video_path);

        var video = '<video src=" ' + data[i].video_path + ' "/>';


        // img_msg = '<img src=" ' + content + '"   data-url=" ' + msg.content  +'" />';


        $("#test").append(video);


    };
}


function show_important_file_text(data){

    // todo 新增页面元素

    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径

    };
}


function show_theory_video(data){

    // todo 新增页面元素

    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径

    };
}


function show_theory_text(data){

    // todo 新增页面元素

    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径

    };
}

function show_paper_video(data){

    // todo 新增页面元素

    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径

    };
}


function show_paper_text(data){

    // todo 新增页面元素

    for(var i = 0; i < data.length; i++){

        // todo 新增html add到 当前页面
        // i.title; 标题
        // i.content 内容
        // i.video_path 视频路径

    };
}


function get_important_file_video(){
  $.ajax({
        url: '/important_file_video',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_important_file_video(data.data);
        },
        error : function() {
          alert("异常！");
        }

    });
}



function get_important_file_text(){
  $.ajax({
        url: '/important_file_text',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_important_file_text(data.data);
        },
        error : function() {
          alert("异常！");
        }

    });
}


function get_theory_video(){
  $.ajax({
        url: '/theory_video',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_theory_video(data.data);
        },
        error : function() {
          alert("异常！");
        }

    });
}


function get_theory_text(){
  $.ajax({
        url: '/theory_text',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_theory_text(data.data);
        },
        error : function() {
          alert("异常！");
        }

    });
}


function get_paper_video(){
  $.ajax({
        url: '/paper_video',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_paper_video(data.data);
        },
        error : function() {
          alert("异常！");
        }
    });
}


function get_paper_text(){
  $.ajax({
        url: '/paper_text',
        processData: false,
        cache: false,
        async: false,
        contentType: false,
        //关键是要设置contentType 为false，不然发出的请求头 没有boundary
        //该参数是让jQuery去判断contentType
        type: "GET",
        success: function(data, status, request) {
            // alert(data.data);
            show_paper_text(data.data);
        },
        error : function() {
          alert("异常！");
        }

    });
}




