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

        <!-- Dependent Info -->
        <input class="formField" v-model="dependentInfo.one.firstName" style="top: 396px; left: 55px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.one.lastName" style="top: 396px; left: 227px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.one.ssn.first" style="top: 396px; left: 342px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.one.ssn.second" style="top: 396px; left: 378px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.one.ssn.third" style="top: 396px; left: 405px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.one.relationship" style="top: 396px; left: 465px; font-size: 14px" size="50" disabled>

        <input class="formField" v-model="dependentInfo.two.firstName" style="top: 413px; left: 55px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.two.lastName" style="top: 413px; left: 227px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.two.ssn.first" style="top: 413px; left: 342px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.two.ssn.second" style="top: 413px; left: 378px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.two.ssn.third" style="top: 413px; left: 405px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.two.relationship" style="top: 413px; left: 465px; font-size: 14px" size="50" disabled>

        <input class="formField" v-model="dependentInfo.three.firstName" style="top: 430px; left: 55px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.three.lastName" style="top: 430px; left: 227px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.three.ssn.first" style="top: 430px; left: 342px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.three.ssn.second" style="top: 430px; left: 378px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.three.ssn.third" style="top: 430px; left: 405px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.three.relationship" style="top: 430px; left: 465px; font-size: 14px" size="50" disabled>

        <input class="formField" v-model="dependentInfo.four.firstName" style="top: 447px; left: 55px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.four.lastName" style="top: 447px; left: 227px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.four.ssn.first" style="top: 447px; left: 342px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.four.ssn.second" style="top: 447px; left: 378px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.four.ssn.third" style="top: 447px; left: 405px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="dependentInfo.four.relationship" style="top: 447px; left: 465px; font-size: 14px" size="50" disabled>


        <!-- Money Info -->
        <input class="formField" v-model="money.one" style="top: 463px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.twoB" style="top: 479px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.threeB" style="top: 496px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.fourB" style="top: 513px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.fourD" style="top: 529px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.fiveB" style="top: 547px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.six" style="top: 563px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.sevenA" style="top: 579px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.sevenB" style="top: 596px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.eightA" style="top: 613px; left: 700px; font-size: 14px" size="50" disabled>
        <input class="formField" v-model="money.eightB" style="top: 629px; left: 700px; font-size: 14px" size="50" disabled>




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
                    third: 6666
                }
            },
            dependentInfo: {
                one: {
                    firstName: "Rishabh",
                    lastName: "Nayak",
                    ssn: {
                        first: 444,
                        second: 55,
                        third: 6666
                    },
                    relationship: "Child",
                    childCredit: true,
                    otherCredit: true,
                },
                two: {
                    firstName: "Vinod",
                    lastName: "Raman",
                    ssn: {
                        first: 420,
                        second: 69,
                        third: 8008
                    },
                    relationship: "Homie",
                    childCredit: false,
                    otherCredit: true,
                },
                three: {
                    firstName: "Gloria",
                    lastName: "Kang",
                    ssn: {
                        first: 111,
                        second: 22,
                        third: 3333
                    },
                    relationship: "Parent",
                    childCredit: true,
                    otherCredit: false,
                },
                four: {
                    firstName: "Harry",
                    lastName: "Wang",
                    ssn: {
                        first: 123,
                        second: 45,
                        third: 6789
                    },
                    relationship: "Uncle",
                    childCredit: true,
                    otherCredit: false,
                },
            },
            money: {
                one: 100000,
                twoA: 200,
                twoB: 200000,
                threeA: 300,
                threeB: 300,
                fourA: 400,
                fourB: 4000,
                fourC: 40000,
                fourD: 400000,
                fiveA: 500,
                fiveB: 500000,
                six: 600,
                sevenA: 700,
                sevenB: 700000,
                eightA: 800,
                eightB: 800000,
                nine: 900,
                ten: 1000,
                elevenA: 110,
                elevenB: 110000
            },
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