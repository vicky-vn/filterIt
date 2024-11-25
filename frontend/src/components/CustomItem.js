import React, { useState } from 'react'

function CustomItem({
    index,
    onSave=os=>os,
    _label='',
    _terms=''
}) {

    const [terms, setTerms] = useState(_terms||'')
    const [label, setLabel] = useState(_label||'')

  return (
    <div className='w-full'>
        <div className='w-full bg-gray-100 text-left rounded-md flex flex-row items-center justify-between px-2'>
            <p className='w-full text-left text-sm text-black px-2 py-1'>Custom Information {index+1}</p>
            <p onClick={() => {
                if (terms && label) onSave({terms: terms?.split(',')?.map(i => i.trim()),label})
            }} className='text-sm text-right font-medium text-rose-600 hover:underline cursor-pointer'>Save</p>
        </div>
        <div className='w-full my-2 flex flex-col items-center space-y-1'>
            <input 
                value={label}
                onChange={e => setLabel(e.target.value)}
                type="text" placeholder='Custom Entity label' className='w-full text-left border bg-black rounded-md px-2 py-2 text-sm text-white' />
            <textarea
                value={terms}
                onChange={e => setTerms(e.target.value)}
                className='w-full text-left border bg-black min-h-[100px] resize-none rounded-md px-2 py-2 text-sm text-white'
                placeholder='Separated by comma'
            ></textarea>
        </div>
    </div>
  )
}

export default CustomItem