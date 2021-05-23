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
	ctx.drawImage(image2, 75, 70, 130, 130)
	ctx.font = '35px Calibri'
	ctx.fillStyle = '#9C9B9B'
	ctx.fillText(nameInput.value, 350, 330)  //nampeInput
    ctx.fillText(courseInput.value, 225, 450) //courseInput
	ctx.font = 'bolder 15px Calibri'
	ctx.fillStyle = '#000000'
	ctx.fillText('ID:#' + certificateIdInput.value, 85, 200)  //certificateIdInput
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