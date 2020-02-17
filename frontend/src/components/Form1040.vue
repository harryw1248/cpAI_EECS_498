<template>
    <div>
        <img src="../assets/1040combined.jpg" style="position:absolute; top:0;" />

        <!-- Filing Status -->
        <img v-if="userInfo.filingStatus === 'Single'" class="check" src="../assets/check.png" style="top:90px; left: 132px;" />
        <img v-if="userInfo.filingStatus === 'MFJ'" class="check" src="../assets/check.png" style="top:90px; left: 192px;" />
        <img v-if="userInfo.filingStatus === 'MFS'" class="check" src="../assets/check.png" style="top:90px; left: 311px;" />
        <img v-if="userInfo.filingStatus === 'HOH'" class="check" src="../assets/check.png" style="top:90px; left: 470px;" />
        <img v-if="userInfo.filingStatus === 'QW'" class="check" src="../assets/check.png" style="top:90px; left: 609px;" />

        <!-- User Info -->
        <input class="formField" v-model="userInfo.firstName" style="top: 153px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="userInfo.lastName" style="top: 153px; left: 332px;" size="50" disabled>
        <input class="formField" v-model="userInfo.address.apt" style="top: 219px; left: 584px;" size="50" disabled>
        <input class="formField" v-model="userInfo.address.street" style="top: 219px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="userInfo.address.cityState" style="top: 253px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="userInfo.ssn.first" style="top: 153px; left: 652px;" size="50" disabled>
        <input class="formField" v-model="userInfo.ssn.second" style="top: 153px; left: 696px;" size="50" disabled>
        <input class="formField" v-model="userInfo.ssn.third" style="top: 153px; left: 728px;" size="50" disabled>

        <!-- User Spouse Info -->
        <input class="formField" v-model="spouseInfo.firstName" style="top: 186px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="spouseInfo.lastName" style="top: 186px; left: 332px;" size="50" disabled>
        <input class="formField" v-model="spouseInfo.ssn.first" style="top: 186px; left: 652px;" size="50" disabled>
        <input class="formField" v-model="spouseInfo.ssn.second" style="top: 186px; left: 696px;" size="50" disabled>
        <input class="formField" v-model="spouseInfo.ssn.third" style="top: 186px; left: 728px;" size="50" disabled>

        <!-- Foreign Country Info -->
        <input class="formField" v-model="userInfo.foreignCountry.country" style="top: 285px; left: 54px;" size="50" disabled>
        <input class="formField" v-model="userInfo.foreignCountry.state" style="top: 285px; left: 362px;" size="50" disabled>
        <input class="formField" v-model="userInfo.foreignCountry.po" style="top: 285px; left: 561px;" size="50" disabled>




    </div>
</template>
<script>
export default {
    name: "Form1040",
    data() {
        return {
            debugModal: false,
            userInfo: {
                firstName: "Rishabh",
                lastName: "Nayak",
                address: {
                    street: "6680 Oakhills Drive",
                    cityState: "Bloomfield Hills, MI 48301",
                    apt: 505
                },
                filingStatus: "Single",
                ssn: {
                    first: 111,
                    second: 22,
                    third: 3333
                },
                foreignCountry: {
                    country: "USA",
                    state: "MI",
                    po: 48301,
                },
            },
            spouseInfo: {
                firstName: "Vinod",
                lastName: "Raman",
                ssn: {
                    first: 444,
                    second: 55,
                    third: 666
                }
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