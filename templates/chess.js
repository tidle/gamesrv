const socket = io();

socket.on("connect", () => {
    socket.emit("chess get", { room: "{{ room }}" });
    console.log("sent request");
});

window.onload = function () {
    $("#pb").attr("disabled", true);
    $("#pw").attr("disabled", true);
    var game = new Chess();
    var player = 's';
    function updateStatus() {
        if (game.turn() === "w") {
            $("#whom").html("It is white's turn");
        } else {
            $("#whom").html("It is black's turn");
        }
        if (game.history().length >= 1) {
            var move = game.history({ verbose: true });
            console.log(move);
            move = move[move.length - 1];
            console.log(move);
            $("#board").find('.square-55d63').removeClass('highlight');
            $("#board").find('.square-' + move.from).addClass('highlight');
            $("#board").find('.square-' + move.to).addClass('highlight');
        }
    }
    function onDragStart(_, piece, _, _) {
        if (piece[0] !== player) { return false; }
    }
    function onDrop(source, target) {
        if (player !== game.turn()) { return "snapback"; }

        var move = game.move({
            from: source,
            to: target,
            promotion: 'q' //always promote to q
        });

        if (move === null) { return "snapback"; }

        console.log("sent move", move.san);

        socket.emit("chess move", {
            room: "{{ room }}",
            move: move.san,
            color: move.color,
            fen: game.fen(),
        });

    }
    function onSnapEnd() {
        board.position(game.fen());
        updateStatus();
    }
    var config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    };
    var board = Chessboard("board", config);
    socket.on("chess move", (data) => {
        console.log("got move", data.move);
        if (
            game.turn() == data.color &&
            "{{ room }}" == data.room
        ) {
            game.move(data.move);
            if (game.move !== null) {
                board.position(game.fen());
            }
        }
        setTimeout(function () {
            if (game.game_over()) {
                if (game.in_checkmate()) {
                    alert("Checkmate!");
                } else if (game.in_draw()) {
                    alert("Draw!");
                } else if (game.in_stalemate()) {
                    alert("Stalemate!");
                }
            }
        }, 100);
        updateStatus();
    });
    socket.on("chess get", (data) => {
        b = data.board;
        console.log("got data", data);
        if (b !== "new") {
            board.position(b);
            game = new Chess(b);
        }
        $("#pb").attr("disabled", data.black);
        $("#pw").attr("disabled", data.white);
        $("#pwhite").html(data.wname);
        $("#pblack").html(data.bname);
        $("#status").removeClass("warning").addClass("status").html("Connected to server as a spectator");
        setInterval(function () {
            socket.emit("chess reclock", "{{ room }}");
        }, parseInt("{{ reclock_interval }}"));
        updateStatus();
    });
    socket.on("chess jwhite", () => {
        player = 'w';
        console.log("joined white");
        board.orientation("white");
        $("#status").html("Connected to server as white player");
    });
    socket.on("chess jblack", () => {
        player = 'b';
        console.log("joined black");
        board.orientation("black");
        $("#status").html("Connected to server as black player");
    });
    socket.on("chess owhite", (data) => {
        if (data.room === "{{ room }}") {
            $('#pw').attr("disabled", true);
            $("#pwhite").html(data.name);
            console.log("owhite");
        }
    });
    socket.on("chess oblack", (data) => {
        if (data.room === "{{ room }}") {
            $('#pb').attr("disabled", true);
            $("#pblack").html(data.name);
            console.log("oblack");
        }
    });
    $('#pb').on('click', function () {
        socket.emit("chess jblack", { room: "{{ room }}", name: "{{ name }}" });
        console.log("sent request");
    });
    $('#pw').on('click', function () {
        socket.emit("chess jwhite", { room: "{{ room }}", name: "{{ name }}" });
        console.log("sent request");
    });
}