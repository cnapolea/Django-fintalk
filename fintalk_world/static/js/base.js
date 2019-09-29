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
    indexSlider();
    
    const apiGenerator = () => {
        //Api of stokes

        const sp = document.querySelector('#sp'), 
            dji = document.querySelector('#dji'),
            ndaq = document.querySelector('#ndaq'), 
            rsl = document.querySelector('#rsl'),
            btc = document.querySelector('#btc'), 
            euUsd = document.querySelector('#eu-usd'), 
            gbpUsd = document.querySelector('#gbp-usd'), 
            usdJp = document.querySelector('#usd-jp');

        let sp_symbol = "GSPC",
            dji_symbol = "DJI",
            // ftse_symbol = "UKX",
            nasdaq_symbol = "NDAQ",
            rut_symbol = "RUT";
            // nkk_symbol = "NI225",
            // bond_symbol = "TNX",
            // crude_symbol = "CL=F",
            // gold_symbol = "GC=F";
                   
            const api_sp = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${sp_symbol}&apikey=PNA7JS5UMRI0PG2D`;
            const api_dji = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${dji_symbol}&apikey=PNA7JS5UMRI0PG2D`;
            const api_nasdaq = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${nasdaq_symbol}&apikey=PNA7JS5UMRI0PG2D`;
            const api_rut = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${rut_symbol}&apikey=PNA7JS5UMRI0PG2D`;
            const api_btc = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=PNA7JS5UMRI0PG2D`;
            const api_eu_usd = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey=PNA7JS5UMRI0PG2D`;
            const api_gbp_usd = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=GBP&to_currency=USD&apikey=PNA7JS5UMRI0PG2D`;
            const api_usd_jpy = `https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=PNA7JS5UMRI0PG2D`;
            // const api_nkk = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${nkk_symbol}&apikey=PNA7JS5UMRI0PG2D`;
            // const api_ftse = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${ftse_symbol}&apikey=PNA7JS5UMRI0PG2D`;


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

            // fetch(api_nkk)
            // .then(response => {
            //     return response.json();
            // })
            // .then(data => {
            //     console.log(data);
            // })

            // fetch(api_ftse)
            // .then(response => {
            //     return response.json();
            // })
            // .then(data => {
            //     console.log(data);
            // })

    };

    // apiGenerator();

    // Burger button dropdown menu
    const menuDropDown = () => {
        
        const burgerMenu = document.querySelector('.burger-menu');
        const authLinks = document.querySelectorAll('.auth-links');

        burgerMenu.addEventListener('click', () => {
            console.log(authLinks[0].classList);
            authLinks[0].classList.toggle('burger-active');
        });
    };
    menuDropDown();

};
run_app();