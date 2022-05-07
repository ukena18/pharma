function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const name_change = (pk) =>{
  let name = document.getElementById("name").value;
  let last = document.getElementById("last").value;
  let parent_id = document.getElementById("parent_id").value;
  
  console.log(pk)
  fetch(`http://127.0.0.1:8000/name_change/`,{
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken,
      },
      body:JSON.stringify({"pk":pk,"name":name,"last":last,"parent_id":parent_id})
    })
    .then(response => response.json())
    .then(data =>{
      let name_update = data.name
      let last_update = data.last
      let parent_id_update = data.parent_id
      document.getElementById("name").value = name_update;
      document.getElementById("last").value = last_update;
      document.getElementById("parent_id").value = parent_id_update;
      document.getElementById("name_change").innerHTML = "Updated";
    } )
  
}

// button doing fet api for single order item 
// and then it change html without refreshing 
// it tooks two params p = order.id payment_method = "CASH" or "CARD"
const order_pay = (pk,payment_method) => {
    // console.log(pk,payment_method)
    // it is speacial api for payment
    fetch(`http://127.0.0.1:8000/order_pay/`,{
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken,
          },
          body:JSON.stringify({"pk":pk,"payment_method":payment_method})
        })
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

                    total_amount_element.innerHTML = `${total_amount}`
                    element_remove.remove()
                }
  });

}


// this is for child payment it pays all the amount
const child_pay = (pk,payment_method) => {
    console.log(pk)
    // send child id to the api 
    fetch(`http://127.0.0.1:8000/child_pay/`,{
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken,
      },
      body:JSON.stringify({"pk":pk,"payment_method":payment_method})
    })
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

