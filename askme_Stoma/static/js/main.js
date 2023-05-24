function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".question-vote .btn-arrow-up").on('click', function (ev) {
    const request = new Request(
        'http://127.0.0.1:8000/question_vote_up/',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'question_id=' + $(this).data('id'),
        }
    );
    
    fetch(request).then(
        response => response.json().then(
            response_json => {
                $(this).parents('.question-likes').find('.counter')[0].innerText = String(response_json.new_rating);
            }
        )
    );
});

$(".question-vote .btn-arrow-down").on('click', function (ev) {
    const request = new Request(
        'http://127.0.0.1:8000/question_vote_down/',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'question_id=' + $(this).data('id'),
        }
    );
    
    fetch(request).then(
        response => response.json().then(
            response_json => {
                $(this).parents('.question-likes').find('.counter')[0].innerText = String(response_json.new_rating);
            }
        )
    );
});

$(".answer-vote .btn-arrow-up").on('click', function (ev) {
    console.log('asdasd')
    const request = new Request(
        'http://127.0.0.1:8000/answer_vote_up/',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $(this).data('id'),
        }
    );
    
    fetch(request).then(
        response => response.json().then(
            response_json => {
                $(this).parents('.question-likes').find('.counter')[0].innerText = String(response_json.new_rating);
            }
        )
    );
});

$(".answer .btn-arrow-down").on('click', function (ev) {
    const request = new Request(
        'http://127.0.0.1:8000/answer_vote_down/',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $(this).data('id'),
        }
    );
    
    fetch(request).then(
        response => response.json().then(
            response_json => {
                $(this).parents('.question-likes').find('.counter')[0].innerText = String(response_json.new_rating);
            }
        )
    );
});

$(".check-field").on('click', function (ev) {
    const request = new Request(
        'http://127.0.0.1:8000/check_field/',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $(this).data('id'),
        }
    );
    
    fetch(request).then(
        response => response.json().then(
            response_json => {
                $(this).parent().find('.form-check-label')[0].innerText = String(response_json.new_correct);
            }
        )
    );
});