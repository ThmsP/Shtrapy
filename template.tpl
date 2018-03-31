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

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

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
      Updated : {{date}}
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
      <h3 class="section-heading">Last activities</h3>
      <div class="row">
      {{!head}}
      </div>
    </div>
  </div>
  <div class="section get-help">
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