import React from 'react'
import { Outlet } from 'react-router'

function BodyComponent() {
  return (
    <div className='w-full h-svh bg-gray-500 flex flex-col items-center p-10'>
        <Outlet/>
    </div>
  )
}

export default BodyComponent