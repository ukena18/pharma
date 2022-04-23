console.log("hello world")

const pay_now = (pk,payment_method) => {
    console.log(pk,payment_method)
        fetch(`http://127.0.0.1:8000/order_pay/${pk}/${payment_method}`)
  .then(response => response.json())
  .then(data =>{
      if (data["result"]=="success"){
          const id = data["id"]
          const total_amount = data['total-amount']
          console.log(id)
          const element_remove = document.getElementById(`person-div-${id}`)
          const total_amount_element = document.getElementById('show-total-amount')
          total_amount_element.innerHTML = total_amount
          element_remove.remove()
      }
  });

}


const child_pay = (pk) => {
    console.log(pk)
    fetch(`http://127.0.0.1:8000/child_pay/${pk}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
      if (data["result"]=="success"){
          const id = data["id"]
          console.log(id)
          const element_remove = document.getElementById(`person-div-${id}`)
          console.log(element_remove)
          element_remove.remove()
      }
  });
}