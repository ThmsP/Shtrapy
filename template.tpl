<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>Skeleton: Responsive CSS Boilerplate</title>
  <meta name="description" content="">
  <meta name="author" content="">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- FONT
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link href='//fonts.googleapis.com/css?family=Raleway:400,300,600' rel='stylesheet' type='text/css'>

  <!-- CSS
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="stylesheet" href="/static/css/normalize.css">
  <link rel="stylesheet" href="/static/css/skeleton.css">
  <link rel="stylesheet" href="/static/css/custom.css">

  <!-- Scripts
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="icon" type="image/png" href="/static/images/favicon.png">

</head>
<body>

  <script>
    function on() {
      
      var ifr = document.getElementsByName('Right')[0];
      ifr.src = ifr.src;
      document.getElementById("overlay").style.display = "block";
    }

    function off() {
      document.getElementById("overlay").style.display = "none";
    }
  </script>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <nav>
    <div class="container">
      <div class="one-third column values-nav u-pull-center">
        <form action="" method="post">
          <button class="button-primary" name="foo" value="Update">Update (last : 20:36)</button>
        </form>
      </div>
      <div class="one-third column values-nav u-pull-center">
        616km this year ! Shut up legs, keep going !
      </div>
      <div class="one-third column values-nav u-pull-center">
        <meter min="0" low="1000." high="4000." max="{{'%.0f'%km_ym1}}" value="{{'%.0f'%km_y}}"> {{km_y}} kilometers</meter> 
        {{'%.0f'%km_y}}km this year ! Shut up legs, keep going !
      </div>
    </div>
  </nav>


  <div class="section values">

    <div class="container">
      
      <div class="row">
        <div class="one-third column value">
          <h2 class="value-multiplier">{{'%.0f'%km_y}}</h2>
          <h5 class="value-heading">Kilometers this year</h5>
          <h2 class="value-multiplier">{{'%.0f'%km_t}}</h2>
          <h5 class="value-heading">Kilometers from all time</h5>
        </div>
        <div class="one-third column value">
          <h2 class="value-multiplier">{{num_activities_y}}</h2>
          <h5 class="value-heading">Actvities</h5>
        </div>
        <div class="one-third column value">
        <a class="weatherwidget-io" href="https://forecast7.com/fr/48d802d26/clamart/" data-label_1="CLAMART" data-label_2="Meteo" data-days="3" >CLAMART Meteo</a>
        <script>
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
        </script>
        </div>
      </div>
      
      <form action="" method="post">
      <button class="button-primary" name="foo" value="Update">Update</button>
      </form>
      <form action="" method="post">
      <button class="button-primary" name="bar" value="AHA">Switch user</button>
      </form>
      Test post : {{test}}
      <form action="" method="post">
      <button class="button-primary" name="bar" value="AHA">YOUYOUY</button>
      </form>
      Test post : YOUYOU TEST
    </div>
  </div>

   <div class="section get-help">
    <div class="container">
      <div class="row">
        <div class="one-half column value">
          <iframe src="/static/parser.html"></iframe>
        </div>
        <div class="one-half column value">
          lblblblblb
        </div>
      </div>
    </div>
  </div>

  <div class="section values">
    <div id="overlay" class="section" >
       <button onclick="off()" class="button-primary button-close">X</button>
       <iframe name="Right" src="/static/parser.html"></iframe>
    </div>
    <div>
      <h2>Test du overlay</h2>
      <button onclick="on()" class="button-primary ">Turn on overlay effect</button>
    </div>
  </div>

  <iframe name="votar" style="display:none;"></iframe>

  <div class="section get-help">
    <div class="container">
      <h3 class="section-heading">Last activities</h3>
      <div class="row">
      {{!head}}
      </div>
    </div>
  </div>

  <div class="section values">
    <div class="container">
      <h3 class="section-heading">A few graphs</h3>
<!--       <p class="section-description">
      
      </p> -->
      % for xml_img in images :
        <div class="row">
        <embed type="image/svg+xml" src= {{xml_img}} />
        </div>
      %end
     <!--  <a class="button button-primary" href="http://getskeleton.com">View Skeleton Docs</a>  -->
    </div>
  </div>





<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>