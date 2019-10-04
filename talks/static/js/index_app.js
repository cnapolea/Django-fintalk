const indexApp = () => {
    //Responsive input field functionality
    const talkField = () => {
        const searchBar = document.querySelector('.search-bar');

        if (window.XMLHttpRequest) {
            var xhttp = new XMLHttpRequest();

            searchBar.addEventListener('input', () => {
                
                xhttp.open('GET', `/ajax/talk_request?${searchBar.name}=${searchBar.value}`, true);                

                xhttp.onreadystatechange = () => {
                    if (xhttp.readyState == 4 && xhttp.status == 200) {
                        let response = JSON.parse(xhttp.responseText);
                        console.log(response);
                    // } else {
                    //     console.log(xhttp.responseText);
                    }
                    
                };
                xhttp.send();
                console.log(searchBar.value);
            });
        }

    }

    talkField();

};
indexApp();