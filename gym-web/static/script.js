const swiper = new Swiper('.slider-wrapper', {

  loop: true,
  grabCursor: true,
  spaceBetween:10,

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  breakpoints: {
        0: {
            slidesPerView: 1,
        },

        768: {
            slidesPerView: 2,
            width: null, // Remove fixed width on mobile
            centeredSlides: true
        },
       
        1024: {
            slidesPerView: 3,
            // width: 300,
            centeredSlides: false
        }
    }

});

const bars = document.querySelector('.fa-bars');
const navLinks = document.querySelector('.nav-links');
const xmark =document.querySelector('.fa-xmark');

bars.addEventListener('click',()=> {
    navLinks.classList.add('active');
    xmark.classList.add('active');
    bars.classList.add('none');
})

const navItems = document.querySelectorAll('.nav-links a'); 

function closeMenu() {
  navLinks.classList.remove('active');
  xmark.classList.remove('active');
  bars.classList.remove('none');
}

xmark.addEventListener('click', closeMenu);

navItems.forEach(item => {
  item.addEventListener('click', closeMenu);
});

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('navbar-scroll');
  } else {
    navbar.classList.remove('navbar-scroll');
  }
});