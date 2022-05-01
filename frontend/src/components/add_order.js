
import React, {useState,useEffect,useContext} from 'react';
import { Routes, Route, useParams } from 'react-router-dom';
import AuthContext from '../context/AuthContext'


function Add_order() {
    const [name,setName] = useState("Person name");
    const [last,setLast] = useState("person last");
    const [customer,setCustomer] = useState(null);
    const [parent,setParent] = useState(null);
    let {authTokens, logoutUser} = useContext(AuthContext)
    let { pk } = useParams();

    //  get user for add_order so we know who we craete an order for
    const getUser = async () => { 
        const response = await fetch(`http://127.0.0.1:8000/api/add_order/${pk}`,{
        method: "GET",
        headers: {
            "Content-Type":"application/json",
            "Authorization":"Bearer "+String(authTokens?.access)
        },
        
        })

        const data = await response.json()
        console.log(data)
        setName(()=>data?.customer.name)
        setLast(()=>data?.customer.last)
        setCustomer(data?.customer)
        setParent(data?.parent)

    }
    // send order to bacend 
    const add_order_api = async (e) => { 
        e.preventDefault()
        const response = await fetch(`http://127.0.0.1:8000/api/add_order/${pk}`,{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
            "Authorization":"Bearer "+String(authTokens.access)
        },
        body: JSON.stringify(
            {description:"description",price:"price"}
        ),
        body: JSON.stringify({description:e.target.description.value,
                            price:e.target.price.value,
                            is_paid:e.target.is_paid.value,
                            who_paid:e.target.whoPaid.value,
                            payment_method:e.target.paymentMethod.value,
                }),
        })
        const data = await response.json()
        

    }

    useEffect(()=>{
        getUser()
    },[])
    return (
        
        <div>
            <form className="add-order-form" onSubmit={add_order_api}>
                    <div className="add-order-container">
                    <label htmlFor="name">Name:</label>
                    <input  className="input-text" type="text" id="name" name="name" value={name} onChange={(e)=>setName(e.target.value)} />
                    
                    <label htmlFor="last">Last:</label>
                    <input  className="input-text" type="text" id="last" name="last" value={last} onChange={(e)=>setLast(e.target.value)} />
                    
                    <label htmlFor="description">Descr:</label>
                    <input  className="input-text" type="text" id="description" name="description" placeholder="description" required />
                
                    <label htmlFor="price">Price:</label>
                    <input  className="input-text" type="text" id="price" name="price" placeholder="price" required />
                    
                    <label for="is_paid">Is paid: </label>
                    <input  class="input-text" type="checkbox" id="is_paid" name="is_paid"/>

                    <label htmlFor="whoPaid">Who paid:</label>
                    <input  className="input-text" type="text" id="whoPaid" list="whoPaid_list" name="whoPaid" placeholder="Who Paid" />
                    <datalist id="whoPaid_list">
                        <option value={customer?.name} />
                        <option value={parent?.name} />
                    </datalist>
                
                    <label htmlFor="paymentMethod">Method: </label>
                    <input  className="input-text" type="text" list="paymentMethod_list" id="paymentMethod" name="paymentMethod"/>
                    <datalist id="paymentMethod_list">
                        <option value="CASH" />
                        <option value="CARD" />
                    </datalist>

                    <button className="add-button search-button">ADD</button>
                </div>
            </form>
        </div>
    
    );
  }
  
  export default Add_order;