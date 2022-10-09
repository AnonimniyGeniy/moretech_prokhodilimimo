<?php 
    session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="../bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="../css/styles.css">
	<script type="text/javascript" src="../bootstrap/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="../js/jquery.js"></script>
	<script type="text/javascript" src="../CONFIG.js"></script>
    <script type="text/javascript">
        let lastloaded = 0;
        let blocksize = 10;
        let role = `
            <?php
                if(!isset($_SESSION['role'])){
                    $_SESSION['role'] = 0;
                }
                echo $_SESSION['role'];
            ?>
        `.trim();
        let rolestr = `
            <?php
                if($_SESSION['role'] == 0){
                    echo 'dir';
                }
                else{
                    echo 'buh';
                }
            ?>
        `.trim();


        
        function loadroles(){
            let rolekey = Object.keys(roles);
            for(let i = 0; i < rolekey.length; i++){
                $("#roledropdown").append(`
                <li class="nav-brand">
                <a class="nav-link">` + 
                roles[rolekey[i]] + 
                `</a></li>`);
            }
        }
        function truncate(input) {
            if (input.length > 100) {
                return input.substring(0, 100) + '...';
            }
            return input;
        };
        let texts;
        function loadnews(){
            keys = Object.keys(obj);
            for(let i = lastloaded; i < Math.min(keys.length, lastloaded + blocksize); i++){
                if(obj[keys[i]]['title'] == undefined || obj[keys[i]]['relevant'][rolestr] < 0.7){
                    continue;
                }

                // <p class="card-text">` + truncate(obj[keys[i]]['text']) + `</p>
                let result = `
                <div class="card text-black bg-white">
                    <div class="card-body">
                        <h5 class="card-title">` + obj[keys[i]]['title'] + `</h5>
                        <small>
                            <a href="` + obj[keys[i]]['link'] + `" class="card-link">Источник</a>
                        </small>
                    </div>
                </div>
                `;
                $("#cardarea").append(result);
            }
            lastloaded += blocksize;
        }
        window.onscroll = function(ev) {
            if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
                loadnews();
            }
        };
        $.ajax({
            method: 'get',
            url: '../php/getdata.php',
            data: {
                'link': '../data/done_data.json'
            },
            success: function(data) {
                obj = JSON.parse(data)['items'];

                keys = Object.keys(obj);
                texts = obj;
                loadnews();
                loadnews();
                loadnews();
                loadnews();
                loadnews();
            }
        });
    </script>
	<title></title>
</head>
    <body>
        <nav class="navbar navbar-expand-light navbar-light bg-light" id = "navbar">
            <div class="container-fluid">
                <label class="navbar-brand" id = "mainlabel">ВТБ</label>
                <a class="nav-link active" aria-current="page" onclick="window.location.reload()" style="cursor:pointer">
                    <image src = "../images/logo.png" id = "image_navbar"/>
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarScroll">
                    <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;" id = "roledropdown">
                    
                    </ul>
                </div>
            </div>
        </nav>
        <div id = 'cardarea'>
        
        </div>
    </body>
</html>
<script>
    loadroles();
    $('#mainlabel').text('ВТБ');
    document.title = roles[role];
</script>