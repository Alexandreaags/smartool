<?php
class Arduino {
    public $link = '';

    function __construct($data_1, $data_2, $data_3, $data_4, $data_5, $data_6, $data_7, $data_8, $data_9, $data_10) {
        $this->connect();
        $this->storeInDB($data_1, $data_2, $data_3, $data_4, $data_5, $data_6, $data_7, $data_8, $data_9, $data_10);
        $this->closeConnection();
    }

    function connect() {
        $this->link = mysqli_connect('p:localhost', 'root', 'ipk123456') or die('Cannot connect to the DB');
        mysqli_select_db($this->link, 'arduino') or die('Cannot select the DB');
    }
    

    function storeInDB($data_1, $data_2, $data_3, $data_4, $data_5, $data_6, $data_7, $data_8, $data_9, $data_10) {
        $data_1 = mysqli_real_escape_string($this->link, $data_1);
        $data_2 = mysqli_real_escape_string($this->link, $data_2);
        $data_3 = mysqli_real_escape_string($this->link, $data_3);
        $data_4 = mysqli_real_escape_string($this->link, $data_4);
        $data_5 = mysqli_real_escape_string($this->link, $data_5);
        $data_6 = mysqli_real_escape_string($this->link, $data_6);
        $data_7 = mysqli_real_escape_string($this->link, $data_7);
        $data_8 = mysqli_real_escape_string($this->link, $data_8);
        $data_9 = mysqli_real_escape_string($this->link, $data_9);
        $data_10 = mysqli_real_escape_string($this->link, $data_10);

        $query = "INSERT INTO sql_data SET 
                  data_1='$data_1', data_2='$data_2', data_3='$data_3', data_4='$data_4', 
                  data_5='$data_5', data_6='$data_6', data_7='$data_7', data_8='$data_8', 
                  data_9='$data_9', data_10='$data_10'";

        $result = mysqli_query($this->link, $query) or die('Errant query: ' . $query);
    }
}

if (
    isset($_GET['data_1']) && isset($_GET['data_2']) && isset($_GET['data_3']) &&
    isset($_GET['data_4']) && isset($_GET['data_5']) && isset($_GET['data_6']) &&
    isset($_GET['data_7']) && isset($_GET['data_8']) && isset($_GET['data_9']) &&
    isset($_GET['data_10'])
) {
    $arduino = new Arduino(
        $_GET['data_1'], $_GET['data_2'], $_GET['data_3'], $_GET['data_4'], $_GET['data_5'],
        $_GET['data_6'], $_GET['data_7'], $_GET['data_8'], $_GET['data_9'], $_GET['data_10']
    );
}
?>
