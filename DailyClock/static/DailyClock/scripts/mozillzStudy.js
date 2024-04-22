let  myheading = document.querySelector('h1')
myheading.textContent = 'HelloWorld'

document.querySelector('html').addEventListener("click", ()=>{
    alert(123)
})

let myimg = document.querySelector('img')
myimg.onclick = ()=>{
    let myscr = myimg.getAttribute('src')
    alert(myscr)
    // alert(456)
}

let mybtn = document.querySelector('button')
let myhead1 = document.querySelector("h1")

function setusername(){
    let myname = prompt('请输入你的名字')
    localStorage.setItem('name',myname)
    myhead1.textContent = "Mozilla 酷毙了，" + myname
    // localStorage.setItem('name',null)
}

if (!localStorage.getItem('name')){
    setusername()
}else {
    let storename= localStorage.getItem('name')
    myhead1.textContent = "Mozilla 酷毙了，" + storename
}

mybtn.onclick = ()=>{
    setusername()
}