//Responsive input field functionality
const talkField = () => {
    const searchBar = document.querySelector('.search-bar');
    const possibleTalks = document.querySelector('.possible-talks');
    const searchResult = document.querySelector('.search-result');
    var resultList;
    
    /* This function organizes and manages the data retrived from the response the ajax request got from the server*/
    const manageAjaxResponse = response => {
        if (response['matchedTalks'] == null) {
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
        let xhttp = new XMLHttpRequest();

        searchBar.addEventListener('input', () => {
            searchResult.innerHTML='';
            xhttp.open('GET', `/ajax/talk_request?talk-name-input=${searchBar.value}`, true);                

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

};

format_date = (date)  => {
    /* This function helps format an unformatted datetime string to [Weekday], [month] [date] at [time]*/

    let date_obj = new Date(date);
    full_date = date_obj.toString(),
    weekday = full_date.slice(0,3),
    month_date = full_date.slice(4,10),
    time = full_date.slice(16,21);

    let formatted_date = `${weekday}, ${month_date} at ${time}`;
    return formatted_date;
};

const homepagePagination = () => {
    const doc = document.documentElement,
        recentTopics = document.querySelector('.recent-topics');

    get_next_page_topics = results => {
        for (index in results) {
            let result = results[index];
            let topicBoard = document.createElement('div'),
                topicLink = document.createElement('a'),
                boardHeader = document.createElement('div'),
                userAvatar = document.createElement('img'),
                headerInfo = document.createElement('p'),
                username = document.createElement('span'),
                talkName = document.createElement('span'),
                boardBody = document.createElement('div'),
                boardFooter = document.createElement('div'),
                commentSection = document.createElement('div'),
                commentIcon = document.createElement('img'),
                numberOfComments = document.createElement('span'),
                timeStamp = document.createElement('span');

            

            userAvatar.setAttribute('src', '/static/image/user-circle-regular.svg');
            commentIcon.setAttribute('src', '/static/image/comment-alt-regular.svg');

            userAvatar.setAttribute('alt', 'User Avatar');

            topicBoard.setAttribute('class','topic-board');
            boardHeader.setAttribute('class','board-header');
            userAvatar.setAttribute('class','user-avatar');
            talkName.setAttribute('class','talk-name');
            boardBody.setAttribute('class','board-body');
            boardFooter.setAttribute('class','board-footer');
            commentSection.setAttribute('class','comment-section');
            commentIcon.setAttribute('class','cmt-icon');
            timeStamp.setAttribute('class','timestamp');

            username.textContent =  `${result[1]} - post at: `;
            talkName.textContent = result[0];
            boardBody.textContent = `${result[2].slice(0, 150)}...`;
            numberOfComments.textContent = result[4];

            timeStamp.textContent = format_date(result[3]);

            recentTopics.appendChild(topicBoard);
            
            topicBoard.appendChild(topicLink);
            
            topicLink.appendChild(boardHeader);
            topicLink.appendChild(boardBody);
            topicLink.appendChild(boardFooter);

            boardHeader.appendChild(userAvatar);
            boardHeader.appendChild(headerInfo);

            headerInfo.appendChild(username);
            headerInfo.appendChild(talkName);

            commentSection.appendChild(commentIcon);
            commentSection.appendChild(numberOfComments);

            boardFooter.appendChild(commentSection);
            boardFooter.appendChild(timeStamp);
        }                            
    };

    let xhttp = new XMLHttpRequest();
    let page_num = 2;

    window.addEventListener('scroll', () => {
        try {
                if (doc.scrollHeight - doc.scrollTop == doc.clientHeight) {   
                    xhttp.open('GET', `/ajax/page_request?page=${page_num}`, true);
                    xhttp.onreadystatechange = () => {
                        if (xhttp.readyState == 4 && xhttp.status == 200) {
                            let response = JSON.parse(xhttp.responseText);
                            let results = response.posts;
                            get_next_page_topics(results);
                        }
                    }
                    xhttp.send();
                    page_num ++;
                }
            } catch(error) {
            console.log(error);
        } 
    });
};

homepagePagination();
talkField();