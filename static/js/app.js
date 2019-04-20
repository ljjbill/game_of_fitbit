function postResult() {
    var url = "/api/viatals";
    d3.json(url).then(function(response) {
        console.log(response);
    })
}