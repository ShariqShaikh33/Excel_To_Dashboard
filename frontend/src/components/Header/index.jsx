import React from 'react'
import NavigateButton from '../common/NavigateButton/NavigateButton'

function Header() {
  const NavArr = [
    {name:"Gender",url:"section1"},
    {name:"Education",url:"section2"},
    {name:"Employment",url:"section3"}
  ]
  return (
    <div className='flex flex-col w-full h-30'>
        <header className='border w-full h-full bg-blue-300'>hello</header>
        <div className='border w-full h-10 bg-blue-700 '>

        <nav>
            <ul className='flex gap-5'>
              {
                NavArr.map((i)=>{
                  return <NavigateButton key={i.name} name={i.name} url={i.url}/>
                })
              }
            </ul>
        </nav>
        </div>
    </div>
  )
}

export default Header