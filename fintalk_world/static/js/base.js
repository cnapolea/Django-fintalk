const run_app = () => {


    // Index slider funtionality
    const indexSlider = () => {
        
        // slider fuctionality
        const leftArrow = document.querySelector('#slide-left');
        const rightArrow = document.querySelector('#slide-right');
        const indexLst1 = document.querySelector('#index-lst1');
        const indexLst2 = document.querySelector('#index-lst2');

        let counter = 0;
    
        leftArrow.addEventListener('click', () => {
            if (counter < 1){
                rightArrow.removeAttribute('disabled', '');
                rightArrow.style.opacity = '1';
                leftArrow.style.opacity = '.5';
                indexLst1.style.transform = `translateX(-200vw)`;
                indexLst2.style.transform = `translateX(-100vw)`;
                counter ++;
                leftArrow.setAttribute('disabled', '');
            }
        });

        rightArrow.addEventListener('click', () => {
            if (counter == 1){
                leftArrow.removeAttribute('disabled', '');
                leftArrow.style.opacity = '1';
                rightArrow.style.opacity = '.5';
                indexLst1.style.transform = `translateX(0vw)`;
                indexLst2.style.transform = `translateX(0vw)`;
                counter --;
                rightArrow.setAttribute('disabled', '');
            }
        });

    };
    
    const apiGenerator = () => {
        //Api of stokes
        const API_KEY_QL = 'yL75LomZDucQi96U23Ln',
            API_KEY_AV = 'PNA7JS5UMRI0PG2D';

        const QL_COMMODITY_URL = `https://www.quandl.com/api/v3/datasets/ODA/PALLFNF_INDEX.json?api_key=${API_KEY_QL}`;
        const AV_BASE_URL = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${API_KEY_AV}`;

        const sp = document.querySelector('#sp'), 
            dji = document.querySelector('#dji'),
            ndaq = document.querySelector('#ndaq'), 
            rsl = document.querySelector('#rsl'),
            btc = document.querySelector('#btc'), 
            euUsd = document.querySelector('#eu-usd'), 
            gbpUsd = document.querySelector('#gbp-usd'), 
            usdJp = document.querySelector('#usd-jp');

        let sp_thicker= "SPX",
            dji_thicker = "DJIA",
            nasdaq_thicker = "COMP",
            rut_thicker = "RUT",
            nkk_thicker = "NIK";
            
<<<<<<< Updated upstream
                   
           


            fetch(api_sp)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let openPrice = +data["Global Quote"]['02. open'];
                sp.textContent = openPrice.toFixed(2);
            })

            fetch(api_dji)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let openPrice = +data["Global Quote"]['02. open'];
                dji.textContent = openPrice.toFixed(2);
            })

            fetch(api_nasdaq)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let openPrice = +data["Global Quote"]['02. open'];
                ndaq.textContent = openPrice.toFixed(2);
            })

            fetch(api_rut)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let openPrice = +data["Global Quote"]['02. open'];
                rsl.textContent = openPrice.toFixed(2);
            })

            fetch(api_btc)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let exgRate = +data["Realtime Currency Exchange Rate"]['5. Exchange Rate'];
                btc.textContent = exgRate.toFixed(2);
            })

            fetch(api_eu_usd)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let exgRate = +data["Realtime Currency Exchange Rate"]['5. Exchange Rate'];
                euUsd.textContent = exgRate.toFixed(2);
            })

            fetch(api_gbp_usd)
            .then(response => {
                return response.json();
            })
            .then(data => {
                let exgRate = +data["Realtime Currency Exchange Rate"]['5. Exchange Rate'];
                gbpUsd.textContent = exgRate.toFixed(2);
            })

            fetch(api_usd_jpy)
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data)
                let exgRate = +data["Realtime Currency Exchange Rate"]['5. Exchange Rate'];
                usdJp.textContent = exgRate.toFixed(2);
            })

            
=======
            for ([ticker, index] of indexes_entry) {
                try {
                    const AV_INDEX_BASE_URL = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${ticker}&apikey=${API_KEY_AV}`;
                    fetch(AV_INDEX_BASE_URL)
                    .then(response => {
                        return response.json();
                    })
                    .then(data => {
                        let openPrice = +data["Global Quote"]["05. price"];
                        index.textContent = openPrice.toFixed(2);
                    })
                } catch (error) {
                    index.textContent = 'Not Available';
                }
            };
        })();

        (get_currency = () => {
            let currencies_entry = Object.entries(Currencies);
            for ([ticker, index] of currencies_entry) {
                try {
                    const AV_CURRENCY_BASE_URL = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=${ticker.slice(0,3)}&to_currency=${ticker.slice(-3,)}&apikey=${API_KEY_AV}`;
                    fetch(AV_CURRENCY_BASE_URL)
                    .then(response => {
                        return response.json();
                    })
                    .then(data => {
                        let exgRate = +data["Realtime Currency Exchange Rate"]["5. Exchange Rate"];
                        index.textContent = exgRate.toFixed(2);
                    })
                } catch (error) {
                    index.textContent = 'Not Available';
                }
                
            };
        })();
        
>>>>>>> Stashed changes
    };

    // Burger button dropdown menu
    const menuDropDown = () => {
        
        const burgerMenu = document.querySelector('.burger-menu');
        const authLinks = document.querySelectorAll('.auth-links');

        burgerMenu.addEventListener('click', () => {
            console.log(authLinks[0].classList);
            authLinks[0].classList.toggle('burger-active');
        });
    };

    //Arrow dropdown
    const arrowDropDown = () => {
        const arrow = document.querySelector('.drop-icon');
        const navLinks = document.querySelector('.user-nav-menu');

        arrow.addEventListener('click', () => {
            navLinks.classList.toggle('drop-active');
        });
    };

    // apiGenerator();
    indexSlider();
    try {
        arrowDropDown();
    } catch {}
    try {
        menuDropDown();
    } catch {}


};
run_app();