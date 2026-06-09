import React from 'react'
import { Outlet } from 'react-router'
import Header from '../../Header'

function Dashboard() {
  return (
    <div>
      <Header></Header>
      <Outlet/>
    </div>
  )
}

export default Dashboard