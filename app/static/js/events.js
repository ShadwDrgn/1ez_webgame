      $(document).ready(function(){
        socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
        process('get', '/' + $('#myTabs .active .clickable').attr('id'));
        $('#myTabs').on('click', '.clickable', function(e){
          e.preventDefault();
          $('#myTabs .active').removeClass('active');
          $(this).parent().removeClass('inactive');
          $(this).parent().addClass('active');
          process('get','/' + $(this).attr('id'));
        });
        socket.on('connect', function() {
            socket.emit('loggedin', {data: 'I\'m connected!'});
        });
        $('#bodyModal').on('submit', 'form', function(e){
          e.preventDefault();
          process('post', $(this).attr('action'), $(this).serialize());
          $('#bodyModal').modal('hide');
        });
        $('#bodyModal').on('click', '#register', function(e){
          e.preventDefault();
          process('get','/appregister');
        });
        $('#navright').on('click', '#login', function(e){
          e.preventDefault();
          process('get', "/applogin");
        });
        $('#navright').on('click', '#newchar', function(e){
          e.preventDefault();
          process('get', "/characters/new");
        });
        $('#navright').on('click', '#logout', function(e){
          e.preventDefault();
          process('get', '/applogout');
        });
        $('#chat').on('submit', 'form', function(e){
          e.preventDefault();
          socket.emit('chat', {data: $(this).find('input[name="chattext"]').val()});
          $(this).find('input[name="chattext"]').val('');
        });
        $('#navright').on('click','ul#charlist li a i.glyphicon-trash',function(e){
          e.preventDefault();
          process('get', $(this).attr('href'));
        });
        socket.on('chat', function(data){
          $('#chattext').html(data.data);
        });
      });
