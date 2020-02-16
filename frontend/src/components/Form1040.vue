<template>
    <div>
        <img src="../assets/1040combined.jpg" style="position:absolute; top:0;" />
        <input v-model="message" placeholder="Name placeholder" style="position:absolute; 
                                                                        top:150px; 
                                                                        left: 50px; 
                                                                        background-color:rgba(0, 0, 0, 0);">
    </div>
</template>
<script>
export default {
    name: "Form1040",
    data : () => ({
        taxForm: '../assets/1040combined.jpg'

    })
};
</script>
