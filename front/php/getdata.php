<?php
    if ($_GET['link']) {
        $json = file_get_contents($_GET['link']);
        echo $json;
    }
?>