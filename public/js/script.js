<<<<<<< HEAD
let filterOption = document.querySelectorAll('.btn.btn-success.form-check-label')
const checkBoxs = document.querySelectorAll('input[type="checkbox"]')

//get data
const getData = async (url) => {
  const data = await axios.get(url)
  return data
}
//change URL
function change(url){
  window.history.pushState('new','title',url)
}
//filter 
async function filter(brandCheckValues, ramCheckValues) {
  if (filterOption.length == 2) {
    filterOption.forEach(function (item) {
      item.addEventListener('click', async function () {
        if (this.innerText.toLowerCase() == "reset") {
          checkBoxs.forEach(function (checkBox) {
            if (checkBox.value == "all") checkBox.checked = true
            else checkBox.checked = false
          })
        }
        if (this.innerText.toLowerCase() == "apply") {
          const brandCheckedValues = []
          const ramCheckedValues = []
          brandCheckValues.forEach(function (cb) {
            if (cb.checked && cb.value != "all") brandCheckedValues.push(cb.value)
          })
          console.log(brandCheckedValues)
          ramCheckValues.forEach(function (cb) {
            if (cb.checked && cb.value != "all") ramCheckedValues.push(cb.value)
          })
          console.log(ramCheckedValues)
          let url = `/product?brand=${brandCheckedValues}&${ramCheckedValues}`
          const data = await axios.get(url)
          console.log(data)
          if (data) displayItems(data)
        }
      })
    });
  }
}
//display
async function displayItems(dl) {
  //product
  let card = dl.data.products.map(function (product) {
    return `<div class="col-lg-3 col-md-4  pt-md-4 pt-3">
      <div class="card d-md-flex flex-column align-items-center">
        <div class="product-name">${product.name}</div>
        <div class="card-img"> <img
            src="${product.image}"
            alt=""> </div>
        <div class="card-body ">
          <div class="text-muted text-center mt-auto">Available Colors</div>
          <div class="d-flex align-items-center justify-content-center colors my-2">
            <div class="btn-group" data-toggle="buttons" data-tooltip="tooltip" data-placement="right"
              title="choose color"> <label class="btn btn-red form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> <label
                class="btn btn-blue form-check-label active"> <input class="form-check-input" type="radio"
                  autocomplete="off"> </label> <label class="btn btn-green form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> <label
                class="btn btn-orange form-check-label"> <input class="form-check-input" type="radio"
                  autocomplete="off"> </label> <label class="btn btn-pink form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> </div>
          </div>
          <div class="d-flex justify-content-center align-items-center price">
            <div class="del mr-2"><span class="text-dark"></span></div>
            <div class="font-weight-bold ">${product.price} đồng</div>
          </div>
          <div class="text-muted text-center mt-auto"><button class="btn btn-red">Add to cart</button></div>
        </div>
      </div>
      </div>`
  })
  if (card == null) {
    card = `<div class="d-flex justify-content-center align-content-center my-5"><h3>Sản phẩm không tồn tại</h3></div>`
  }
  card = card.join("")
  const productSection = document.querySelector('#productSection')
  productSection.innerHTML = ''
  productSection.innerHTML = card

}
async function checkBoxOnlick(ob) {
  const remnant = []
  let all = null
  ob.forEach(function (cb) {
    if (cb.value == "all") all = cb
    else remnant.push(cb)
  })
  ob.forEach(function (item) {
    item.addEventListener('click', function () {
      if (this.value == "all" && this.checked == true) {
        remnant.map(function (i) {
          i.checked = false
        })
      }
      if (remnant.includes(this) && this.checked == true) {
        all.checked = false
      }
      if (this.checked) { console.log(this.value) }
    })
  })
}
async function pagination(dl){
  //pagination
  const pagination = document.querySelector('.pagination.pg-blue')
  pagination.innerHTML = ''
  const numberOfPage = dl.data.numberOfPage
  const currentPage = dl.data.page
  let i = 1;               
  if (currentPage > 4 && numberOfPage > currentPage) {
    pagination.innerHTML = `<li class="page-item" value="${i}">
                             <a class="page-link" href="#">${i}
                             </a>
                           </li>`
    pagination.innerHTML += `<li class="page-item ">
                             <a class="page-link" href="#">...
                             </a>
                           </li>`
    i= currentPage-2
    while (i<numberOfPage) {
      if (currentPage + 2 >= i && i >= currentPage-2  ) {
        pagination.innerHTM += `<li class="page-item" value="${i}">
                                                        <a class="page-link" href="#">${i}
                                                        </a>
                                                      </li>`
        i++
      }
    }          
    if(i == numberOfPage){
      pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                           <a class="page-link" href="#">${numberOfPage}
                           </a>
                         </li>`   
    }
    else{
      pagination.innerHTML += `<li class="page-item ">
                           <a class="page-link" href="#">...
                           </a>
                         </li>`
      pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                              <a class="page-link" href="#">${numberOfPage}
                              </a>
                            </li>`
    }           
  }
    else{
      while(currentPage<=4 && i <numberOfPage && i<=currentPage+2){
          pagination.innerHTML += `<li class="page-item" value="${i}">
                             <a class="page-link" href="#">${i}
                             </a>
                           </li>`   
          i++                      
      }
      if(i== numberOfPage){
        pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                             <a class="page-link" href="#">${numberOfPage}
                             </a>
                           </li>`   
      }
      else{
        pagination.innerHTML += `<li class="page-item ">
                             <a class="page-link" href="#">...
                             </a>
                           </li>`
        pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                                <a class="page-link" href="#">${numberOfPage}
                                </a>
                              </li>`
      }
    }
  //mark current page
  const pages = document.querySelectorAll('.page-item')
  for(let j = 1;j<=currentPage;j++){
    if(j == currentPage) {
      pages[j-1].classList.add("active")
      break
    } 
  }
  console.log(currentPage)
}
async function switchPage(){
  const btnPages = document.querySelectorAll('.page-item')
  btnPages.forEach(function(btn){
    btn.addEventListener('click',async function(){
      let url = `/product?page=${btn.value}`
      const data = await axios.get(url)
      if(data) {
        displayItems(data)
        pagination(data)
        switchPage()
      }
    })
  }) 
}
window.addEventListener("DOMContentLoaded", async function () {
  try {
    const data =  await getData('/product')
    const brandCheckValues = document.querySelectorAll('input#brand[type="checkbox"]')
    const ramCheckValues = document.querySelectorAll('input#Ram[type="checkbox"]')
    console.log(data)
    displayItems(data)
    pagination(data)
    switchPage()
    checkBoxOnlick(brandCheckValues)
    checkBoxOnlick(ramCheckValues)
    filter(brandCheckValues, ramCheckValues)
  } catch (error) {
    return `${error}`
  }
})


=======
let filterOption = document.querySelectorAll('.btn.btn-success.form-check-label')
const checkBoxs = document.querySelectorAll('input[type="checkbox"]')

//get data
const getData = async (url) => {
  const data = await axios.get(url)
  return data
}
//change URL
function change(url){
  window.history.pushState('new','title',url)
}
//filter 
async function filter(brandCheckValues, ramCheckValues) {
  if (filterOption.length == 2) {
    filterOption.forEach(function (item) {
      item.addEventListener('click', async function () {
        if (this.innerText.toLowerCase() == "reset") {
          checkBoxs.forEach(function (checkBox) {
            if (checkBox.value == "all") checkBox.checked = true
            else checkBox.checked = false
          })
        }
        if (this.innerText.toLowerCase() == "apply") {
          const brandCheckedValues = []
          const ramCheckedValues = []
          brandCheckValues.forEach(function (cb) {
            if (cb.checked && cb.value != "all") brandCheckedValues.push(cb.value)
          })
          console.log(brandCheckedValues)
          ramCheckValues.forEach(function (cb) {
            if (cb.checked && cb.value != "all") ramCheckedValues.push(cb.value)
          })
          console.log(ramCheckedValues)
          let url = `/product?brand=${brandCheckedValues}&${ramCheckedValues}`
          const data = await axios.get(url)
          console.log(data)
          if (data) displayItems(data)
        }
      })
    });
  }
}
//display
async function displayItems(dl) {
  //product
  let card = dl.data.products.map(function (product) {
    return `<div class="col-lg-3 col-md-4  pt-md-4 pt-3">
      <div class="card d-md-flex flex-column align-items-center">
        <div class="product-name">${product.name}</div>
        <div class="card-img"> <img
            src="${product.image}"
            alt=""> </div>
        <div class="card-body ">
          <div class="text-muted text-center mt-auto">Available Colors</div>
          <div class="d-flex align-items-center justify-content-center colors my-2">
            <div class="btn-group" data-toggle="buttons" data-tooltip="tooltip" data-placement="right"
              title="choose color"> <label class="btn btn-red form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> <label
                class="btn btn-blue form-check-label active"> <input class="form-check-input" type="radio"
                  autocomplete="off"> </label> <label class="btn btn-green form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> <label
                class="btn btn-orange form-check-label"> <input class="form-check-input" type="radio"
                  autocomplete="off"> </label> <label class="btn btn-pink form-check-label"> <input
                  class="form-check-input" type="radio" autocomplete="off"> </label> </div>
          </div>
          <div class="d-flex justify-content-center align-items-center price">
            <div class="del mr-2"><span class="text-dark"></span></div>
            <div class="font-weight-bold ">${product.price} đồng</div>
          </div>
          <div class="text-muted text-center mt-auto"><button class="btn btn-red">Add to cart</button></div>
        </div>
      </div>
      </div>`
  })
  if (card == null) {
    card = `<div class="d-flex justify-content-center align-content-center my-5"><h3>Sản phẩm không tồn tại</h3></div>`
  }
  card = card.join("")
  const productSection = document.querySelector('#productSection')
  productSection.innerHTML = ''
  productSection.innerHTML = card

}
async function checkBoxOnlick(ob) {
  const remnant = []
  let all = null
  ob.forEach(function (cb) {
    if (cb.value == "all") all = cb
    else remnant.push(cb)
  })
  ob.forEach(function (item) {
    item.addEventListener('click', function () {
      if (this.value == "all" && this.checked == true) {
        remnant.map(function (i) {
          i.checked = false
        })
      }
      if (remnant.includes(this) && this.checked == true) {
        all.checked = false
      }
      if (this.checked) { console.log(this.value) }
    })
  })
}
async function pagination(dl){
  //pagination
  const pagination = document.querySelector('.pagination.pg-blue')
  pagination.innerHTML = ''
  const numberOfPage = dl.data.numberOfPage
  const currentPage = dl.data.page
  let i = 1;               
  if (currentPage > 4 && numberOfPage > currentPage) {
    pagination.innerHTML = `<li class="page-item" value="${i}">
                             <a class="page-link" href="#">${i}
                             </a>
                           </li>`
    pagination.innerHTML += `<li class="page-item ">
                             <a class="page-link" href="#">...
                             </a>
                           </li>`
    i= currentPage-2
    while (i<numberOfPage) {
      if (currentPage + 2 >= i && i >= currentPage-2  ) {
        pagination.innerHTM += `<li class="page-item" value="${i}">
                                                        <a class="page-link" href="#">${i}
                                                        </a>
                                                      </li>`
        i++
      }
    }          
    if(i == numberOfPage){
      pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                           <a class="page-link" href="#">${numberOfPage}
                           </a>
                         </li>`   
    }
    else{
      pagination.innerHTML += `<li class="page-item ">
                           <a class="page-link" href="#">...
                           </a>
                         </li>`
      pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                              <a class="page-link" href="#">${numberOfPage}
                              </a>
                            </li>`
    }           
  }
    else{
      while(currentPage<=4 && i <numberOfPage && i<=currentPage+2){
          pagination.innerHTML += `<li class="page-item" value="${i}">
                             <a class="page-link" href="#">${i}
                             </a>
                           </li>`   
          i++                      
      }
      if(i== numberOfPage){
        pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                             <a class="page-link" href="#">${numberOfPage}
                             </a>
                           </li>`   
      }
      else{
        pagination.innerHTML += `<li class="page-item ">
                             <a class="page-link" href="#">...
                             </a>
                           </li>`
        pagination.innerHTML += `<li class="page-item" value="${numberOfPage}">
                                <a class="page-link" href="#">${numberOfPage}
                                </a>
                              </li>`
      }
    }
  //mark current page
  const pages = document.querySelectorAll('.page-item')
  for(let j = 1;j<=currentPage;j++){
    if(j == currentPage) {
      pages[j-1].classList.add("active")
      break
    } 
  }
  console.log(currentPage)
}
async function switchPage(){
  const btnPages = document.querySelectorAll('.page-item')
  btnPages.forEach(function(btn){
    btn.addEventListener('click',async function(){
      let url = `/product?page=${btn.value}`
      const data = await axios.get(url)
      if(data) {
        displayItems(data)
        pagination(data)
        switchPage()
      }
    })
  }) 
}
window.addEventListener("DOMContentLoaded", async function () {
  try {
    const data =  await getData('/product')
    const brandCheckValues = document.querySelectorAll('input#brand[type="checkbox"]')
    const ramCheckValues = document.querySelectorAll('input#Ram[type="checkbox"]')
    console.log(data)
    displayItems(data)
    pagination(data)
    switchPage()
    checkBoxOnlick(brandCheckValues)
    checkBoxOnlick(ramCheckValues)
    filter(brandCheckValues, ramCheckValues)
  } catch (error) {
    return `${error}`
  }
})


>>>>>>> b0ab0c5fafafd5c49d8ccba8082c7745ef0dcbba
