const run_app = () => {

    // Index slider funtionality
    const indexSlider = () => {
    
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
};
run_app();