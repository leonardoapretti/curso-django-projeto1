function my_scope(){
    const form = document.querySelector('.form-delete')
    console.log(form)
    
    if(form){
        console.log(form)

        form.addEventListener('submit', function(e){
            e.preventDefault()

            const confirmed = confirm('Are you sure?')

            if(confirmed) form.submit()
        })
    }
}

document.addEventListener('onload', my_scope())