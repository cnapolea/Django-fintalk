const indexApp = () => {
    //Responsive input field functionality
    const talkField = () => {
        const searchBar = document.querySelector('.search-bar');
        const possibleTalks = document.querySelector('.possible-talks');
        const searchResult = document.querySelector('.search-result');
        var resultList;
        
        /* This function organizes and manages the data retrived from the response the ajax request got from the server*/
        const manageAjaxResponse = response => {
            if (response['matchedTalks'] == null) {
                searchResult.innerHTML='';
                possibleTalks.classList.remove('possible-talks-active');

            } else if (typeof response.matchedTalks == 'string') {
                let listItem = document.createElement('li');
                    listItem.textContent = response.matchedTalks;
                    searchResult.appendChild(listItem);
                    possibleTalks.classList.add('possible-talks-active');
            } else {
                
                possibleTalks.classList.add('possible-talks-active');
                for (index in response.matchedTalks) {
                    let listItem = document.createElement('li');
                    listItem.textContent = response.matchedTalks[index];
                    searchResult.appendChild(listItem);
                }
            } 
        };

        const getTalk = resultList => {
            /* This function get the suggestive talk and inserts as the value of the search bar*/

            if (resultList) {
                resultList.forEach(item => {
                    item.addEventListener('click', () => {
                        searchBar.value = item.textContent;
                        possibleTalks.classList.remove('possible-talks-active');
                    });
                });
            }
        };

        if (window.XMLHttpRequest) {
            var xhttp = new XMLHttpRequest();

            searchBar.addEventListener('input', () => {
                
                xhttp.open('GET', `/ajax/talk_request?${searchBar.name}=${searchBar.value}`, true);                

                xhttp.onreadystatechange = () => {
                    if (xhttp.readyState == 4 && xhttp.status == 200) {
                        let response = JSON.parse(xhttp.responseText);
                        
                        manageAjaxResponse(response);
                        
                        resultList = document.querySelectorAll('.search-result li');
                        getTalk(resultList);
                    }
                };
                xhttp.send();
                
            });
        }

        

    }

    talkField();

};
indexApp();