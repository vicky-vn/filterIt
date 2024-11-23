import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Dialog, DialogPanel, DialogTitle, DialogBackdrop } from '@headlessui/react'

function Header() {

    const [openAuthDialog, setOpenAuthDialog] = useState(false)

    const handleAuth = () => {
        setOpenAuthDialog(false)
    }

  return (
    <div className='w-full px-10 py-6 text-md flex flex-row items-center justify-between'>
        <div className='flex items-center space-x-2'>
            <img 
                src='./logo.png'
                alt='logo'
                className='contain h-[30px]'
            />
            <Link to='/'>
            <h1 className='tracking-tighter text-xl text-left text-black font-bold'>filterIt</h1>
            </Link>
        </div>
        <div className='grid grid-cols-4 gap-4'>
            <Link to='/'>
                <p className='text-black text-sm text-center hover:text-gray-600'>Home</p>
            </Link>
            <Link to='/settings'>
                <p className='text-black text-sm text-center hover:text-gray-600'>Settings</p>
            </Link>
            <Link to='/about'>
                <p className='text-black text-sm text-center hover:text-gray-600'>About</p>
            </Link>
            <button 
                onClick={() => setOpenAuthDialog(true)}
                className='transform active:scale-105 duration-200 rounded-md text-xs font-medium text-white bg-black hover:bg-gray-700 text-center px-3 py-1'>
                Sign In
            </button>
        </div>
        <Dialog open={openAuthDialog} as="div" className="relative z-10 focus:outline-none" onClose={() => {}}>
            <DialogBackdrop className="fixed inset-0 bg-black/50" />
            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div className="flex min-h-full items-start justify-center p-4 mt-10">
                    <DialogPanel
                        transition
                        className="w-full max-w-lg rounded-md bg-white p-4 backdrop-blur-2xl duration-100 ease-out data-[closed]:transform-[scale(95%)] data-[closed]:opacity-0"
                    >
                    <DialogTitle as="h3" className="text-md mb-2 font-semibold text-black">
                        Sign In into your account
                    </DialogTitle>
                    <label htmlFor='email' className='text-gray-500 text-left text-xs'>Email Address</label>
                    <input 
                        id='email'
                        type='email'
                        placeholder='Enter Email Address'
                        className='my-1 rounded-md outline-none border w-full text-left text-black text-xs px-3 py-2'
                    />
                    <label htmlFor='password' className='text-gray-500 text-left text-xs'>Password</label>
                    <input 
                        id='password'
                        type='password'
                        placeholder='Enter Password'
                        className='my-1 rounded-md outline-none border w-full text-left text-black text-xs px-3 py-2'
                    />
                    <div className="mt-4">
                        <button 
                            onClick={() => handleAuth()}
                            className='transform active:scale-105 duration-200 bg-black px-2 py-1 text-white text-center text-xs rounded-md mr-2'>Sign In</button>
                        <button 
                            onClick={() => setOpenAuthDialog(false)}
                            className='transform active:scale-105 duration-200 bg-white px-2 py-1 text-black hover:bg-gray-100 text-center text-xs rounded-md mr-2'>Cancel</button>
                    </div>
                    </DialogPanel>
                </div>
            </div>
        </Dialog>
    </div>
  )
}

export default Header
