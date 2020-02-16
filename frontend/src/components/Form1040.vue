<template>
    <div>
        <img src="../assets/1040combined.jpg" style="position:absolute; top:0;" />

        <img v-if="formInfo.filingStatus === 'Single'" class="check" src="../assets/check.png" style="top:90px; left: 132px;" />
        <img v-if="formInfo.filingStatus === 'MFJ'" class="check" src="../assets/check.png" style="top:90px; left: 192px;" />
        <img v-if="formInfo.filingStatus === 'MFS'" class="check" src="../assets/check.png" style="top:90px; left: 311px;" />


        <input class="formField" v-model="formInfo.firstName" style="top: 153px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="formInfo.lastName" style="top: 153px; left: 332px;" size="50" disabled>
        <input class="formField" v-model="formInfo.homeAddress" style="top: 219px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="formInfo.homeCityState" style="top: 253px; left: 54px;" size="50" disabled>
    </div>
</template>
<script>
export default {
    name: "Form1040",
    data() {
        return {
            debugModal: false,
            formInfo: {
                firstName: "Rishabh",
                lastName: "Nayak",
                homeAddress: "6680 Oakhills Drive",
                homeCityState: "Bloomfield Hills, MI 48301",
                filingStatus: "Single"
            }
        };
    },
};
</script>

<style scoped>
.formField {
  position:absolute;
  background-color:rgba(0, 0, 0, 0);
  line-height: 3px;
  color: red;
}

.check {
    position:absolute;
    width: 15px;
}

</style>