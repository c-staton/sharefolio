async function deleteStock(evt){
    evt.preventDefault();
    const id = $(this).parent().parent().data('id');
    console.log('ID: ' + id)
    await axios.delete(`/portfolio/${id}`)
    $(this).parent().parent().parent().remove();
}
$(".delete-portfolio").on('click', deleteStock)