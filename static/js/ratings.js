//initial ratings 
var ratings = {
 
}

// Total stars
var starsTotal = 10;

//Run getRatings when DOM loads
document.addEventListener('DOMContentLoaded',getRatings);

// Form Elements
const criteriaSelect = document.getElementById('criteria-select');
const ratingControl = document.getElementById('rating-control');

// Init product
let criteria;

// Product select change
criteriaSelect.addEventListener('change',(e) => {
  criteria = e.target.value;
  // Enable rating control
  ratingControl.disabled = false;
  ratingControl.value = ratings[criteria];
})

// Rating control change
ratingControl.addEventListener('change', (e) => {
  const rating = e.target.value;

  // Check if 10 or under
  if(rating > 10) {
    alert('Please rate on a scale of 1-10');
    return;
  }

  //Change rating
  ratings[criteria] = rating;

  getRatings();
});

//Get ratings
function getRatings() {
  for(let rating in ratings) {
    // Get percentage
    var starPercentage = (ratings[rating] / starsTotal) * 100;

    // Round to nearest 10
    var starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

    // Set width of stars-inner to percentage
    document.querySelector(`.${rating} .stars-inner`).style.width=starPercentageRounded;

    //Add number rating
    document.querySelector(`.${rating} .number-rating`).innerHTML = ratings[rating];
  }
}