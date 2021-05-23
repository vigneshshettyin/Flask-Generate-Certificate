const canvas = document.getElementById('canvas')
const ctx = canvas.getContext('2d')
const nameInput = document.getElementById('name')
const courseInput = document.getElementById('course')
const certificateIdInput = document.getElementById('certificateId')
const downloadBtn = document.getElementById('download-btn')

const image1 = new Image()
image1.src = './certificate.png'
image1.onload = function () {
	drawImage()
}

const image2 = new Image()
image2.src = './qr_code.png'
image2.onload = function () {
	drawImage()
}

function drawImage() {
	// ctx.clearRect(0, 0, canvas.width, canvas.height)
	ctx.drawImage(image1, 0, 0, canvas.width, canvas.height)
	ctx.drawImage(image2, 30, 450, 130, 130)
	ctx.font = '35px Candara'
	ctx.fillStyle = '#252F5F'
	ctx.fillText(nameInput.value, 320, 230)  //nampeInput
    ctx.fillText(courseInput.value, 220, 395) //courseInput
	ctx.font = 'bolder 15px Calibri'
	ctx.fillStyle = '#000000'
	ctx.fillText('ID:#' + certificateIdInput.value, 40, 580)  //certificateIdInput
}

nameInput.addEventListener('input', function () {
	drawImage()
})
courseInput.addEventListener('input', function () {
	drawImage()
})
certificateIdInput.addEventListener('input', function () {
	drawImage()
})

downloadBtn.addEventListener('click', function () {
	downloadBtn.href = canvas.toDataURL('image/png')
	downloadBtn.download = 'Certificate - ' + nameInput.value + courseInput.value + certificateIdInput.value
})