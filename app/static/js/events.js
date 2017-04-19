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
        $('#bodyModal').on('submit', '#login-nav', function(e){
          e.preventDefault();
          process('post','/login',$(this).serialize());
          $('#bodyModal').modal('hide');
        });
        $('#bodyModal').on('submit', '#register-nav', function(e){
          e.preventDefault();
          $('#bodyModal').modal('hide');
          process('post','/register',$(this).serialize());
        });
        $('#bodyModal').on('click', '#register', function(e){
          e.preventDefault();
          process('get','/signup');
        });
        $('#navright').on('click', '#login', function(e){
          e.preventDefault();
          process('get', "/signin");
        });
        $('#navright').on('click', '#logout', function(e){
          e.preventDefault();
          process('get', '/logout');
        });
        $('#navright').on('click', '#newchar', function(e){
          e.preventDefault();
          //process('get', '/logout');
          alert('Not Implemented yet');
        });
        $('#chat').on('submit', 'form', function(e){
          e.preventDefault();
          socket.emit('chat', {data: $(this).find('input[name="chattext"]').val()});
        });
        socket.on('chat', function(data){
          $('#chattext').html(data.data);
        });
      });
