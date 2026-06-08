import React from 'react'
import { Outlet } from 'react-router'

function Dashboard() {
  return (
    <div>
      <Outlet/>
    </div>
  )
}

export default Dashboard