$(document).ready(function(){
    var quill = new Quill('#editor-container', {
        modules: {
        toolbar: [
            [{ 'font': [] }],
            [{ header: [1, 2, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'indent': '-1'}, { 'indent': '+1' }],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ]
        },
        theme: 'snow'  // or 'bubble'
    });
});