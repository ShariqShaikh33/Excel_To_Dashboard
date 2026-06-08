import React from 'react'

function Header() {
  return (
    <div className='flex flex-col w-full h-50'>
        <header className='border w-full h-full bg-blue-300'>hello</header>
        <div className='border w-full h-10 bg-blue-700 '>

        <nav>
            <ul className='flex gap-5'>
            <li><a>Gender</a></li>
            <li><a>Age</a></li>
            </ul>
        </nav>
        </div>
    </div>
  )
}

export default Header