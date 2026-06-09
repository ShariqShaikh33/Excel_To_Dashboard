import React from 'react'
import { useNavigate } from 'react-router'

function NavigateButton({name,url}) {
    const navigate = useNavigate()
    function goTo(i){
        navigate(i);
    }
  return (
    <div>
        <button onClick={()=>{goTo(url)}}>{name}</button>
    </div>
  )
}

export default NavigateButton