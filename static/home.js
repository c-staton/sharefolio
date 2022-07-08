function animateOnScroll(eleId, animateClass) {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add(animateClass);
        }
        });
    });

    observer.observe(document.getElementById(eleId));
}
  
animateOnScroll('main-img', 'slide-left');
animateOnScroll('first-img', 'slide-right');
animateOnScroll('second-img', 'slide-right');
animateOnScroll('third-img', 'slide-right');

animateOnScroll('main-info', 'fade-in');
animateOnScroll('first-info', 'fade-in');
animateOnScroll('second-info', 'fade-in');
animateOnScroll('third-info', 'fade-in');

  