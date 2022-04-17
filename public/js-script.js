//items
const productSection = document.querySelector('#dataContainer')
checkboxs = document.querySelectorAll('form-check-input')


//load items
window.addEventListener("DOMContentLoaded", async function () {
  try {
    const listItems = await axios.get('/product')   
    console.log(listItems)
    displayItems(listItems)
  } catch (error) {
    
  }
})
//filter items
// checkboxs.array.forEach(function(cb) {
//     cb.addEventListener("click",function(e){
//         const brand = e.currentTarget.value
//         console.log(brand)
//     })
// });

async function displayItems(listItems) {
  let card = listItems.data.products.map(function (product) {
    return `<div class="col-md-4 my-2 my-2 my-2 ">
        <div class="card">
          <div class="card-body">
            <div class="card-img-actions"> <img
                src=${product.image}
                class="card-img img-fluid" width="96" height="350" alt="" alt=${product.name}> </div>
          </div>
          <div class="card-body bg-light text-center">
            <div class="mb-2">
              <h6 class="font-weight-semibold mb-2"> <a href="#" class="text-default mb-2" data-abc="true">${product.name}</a> </h6> <a href="#" class="text-muted"
                data-abc="true">${product.brand}</a>
            </div>
            <h3 class="mb-0 font-weight-semibold">${product.price} đồng</h3>
            <div> <i class="bi bi-star star"></i> <i class="bi bi-star star"></i> <i class="bi bi-star star"></i>
              <i class="bi bi-star star"></i>
            </div>
            <div class="text-muted mb-3">34 reviews</div> <button type="button" class="btn bg-cart btn-warning"><i
                class="bi bi-cart-plus mr-2"></i> Add to cart</button>
          </div>
        </div>
      </div>`
  })
  card = card.join("")
  productSection.innerHTML = card
}