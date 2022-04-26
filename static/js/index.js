// console.log("hello world")



// button doing fet api for single order item 
// and then it change html without refreshing 
// it tooks two params p = order.id payment_method = "CASH" or "CARD"
const pay_now = (pk,payment_method) => {
    // console.log(pk,payment_method)
    // it is speacial api for payment
    fetch(`http://127.0.0.1:8000/order_pay/${pk}/${payment_method}`)
        // jsnoize
        .then(response => response.json())
        // data has result , an id, and the new total amount after it has been paid current order
        .then(data =>{
                if (data["result"]=="success"){
                    const id = data["id"]
                    const total_amount = data['total-amount']
                    // console.log(id)
                    // we remove the eleemnt with id because we paid for it 
                    const element_remove = document.getElementById(`person-div-${id}`)
                    // refreshing total amount
                    const total_amount_element = document.getElementById('show-total-amount')

                    total_amount_element.innerHTML = total_amount
                    element_remove.remove()
                }
  });

}


// this is for child payment it pays all the amount
const child_pay = (pk) => {
    // console.log(pk)
    // send child id to the api 
    fetch(`http://127.0.0.1:8000/child_pay/${pk}`)
    .then(response => response.json())
    // 
    .then(data =>{
        console.log(data)
      if (data["result"]=="success"){
          const id = data["id"]
        //   console.log(id)
        // remove the child 
        const element_remove = document.getElementById(`person-div-${id}`)
        //   console.log(element_remove)
          element_remove.remove()
      }
  });
}