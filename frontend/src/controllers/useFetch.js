import { useState, useEffect } from 'react';

const useFetch = (url) => {
  const [data, setData] = useState(null);
  const [isPending, setIsPending] = useState(true);
  const [error, setError] = useState(null);

//   let getUsers = async() =>{
//     let response = await fetch('http://127.0.0.1:8000/api/search', {
//         method:'GET',
//         headers:{
//             'Content-Type':'application/json',   
//         }
//     })
//     let data = await response.json()    
//     console.log(data)
    
// }
// useEffect(()=>{
//    getUsers()
// },[])

  useEffect(() => {
    // const abortCont = new AbortController();
      fetch(url, {
        method:'GET',
        headers:{
                'Content-Type':'application/json',   
            }  
        // ,signal: abortCont.signal,
     })
      .then(response => {
        if (!response.ok) { // error coming back from server
          throw Error('could not fetch the data for that resource');
        } 
        return response.json();
      })
      .then(data => {
          
        setIsPending(false);
        setData(data);
        setError(null);
      })
      .catch(err => {
        if (err.name === 'AbortError') {
          console.log('fetch aborted')
        } else {
          // auto catches network / connection error
          setIsPending(false);
          setError(err.message);
        }
      })
  

    // abort the fetch
    // return () => abortCont.abort();
  }, [url])

  return { data, isPending, error };
}
 
export default useFetch;