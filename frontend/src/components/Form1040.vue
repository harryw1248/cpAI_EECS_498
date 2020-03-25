<template>
    <div class="relative" style="width: 868px; height: 1476px">
        <!-- 1 -->
        <input
            :value="user_income['wages']"
            class="formField absolute z-30"
            style="top: 468px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 2a -->
        <input
            :value="user_income['tax-exempt-interest']"
            class="formField z-30"
            style="top: 486px; left: 354px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 2b -->
        <input
            :value="user_income['taxable-interest']"
            class="formField z-30"
            style="top: 486px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 3a -->
        <input
            :value="user_income['qualified-dividends']"
            class="formField z-30"
            style="top: 504px; left: 354px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 3b -->
        <input
            :value="user_income['ordinary-dividends']"
            class="formField z-30"
            style="top: 504px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 4a -->
        <input
            :value="user_income['IRA-distributions']"
            class="formField z-30"
            style="top: 520px; left: 354px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 4b -->
        <input
            :value="user_income['IRA-distributions-taxable']"
            class="formField z-30"
            style="top: 520px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 4c -->
        <input
            :value="user_income['pensions-and-annuities']"
            class="formField z-30"
            style="top: 536px; left: 354px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 4d -->
        <input
            :value="user_income['pensions-and-annuities-taxable']"
            class="formField z-30"
            style="top: 536px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 5a -->
        <input
            :value="user_income['ss-benefits']"
            class="formField z-30"
            style="top: 552px; left: 354px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 5b -->
        <input
            :value="user_income['ss-benefits-taxable']"
            class="formField z-30"
            style="top: 552px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 6 -->
        <input
            :value="user_income['capital-gains']"
            class="formField z-30"
            style="top: 568px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 7a -->
        <input
            :value="user_income['other-income']"
            class="formField z-30"
            style="top: 586px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 7b -->
        <input
            :value="user_income['7b']"
            class="formField z-30"
            style="top: 603px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 8a -->
        <input
            :value="user_income['adjustments-to-income']"
            class="formField z-30"
            style="top: 620px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 8b -->
        <input
            :value="user_income['8b']"
            class="formField z-30"
            style="top: 636px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 9 -->
        <input
            class="formField z-30"
            style="top: 652px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 10 -->
        <input
            :value="0"
            class="formField z-30"
            style="top: 670px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 11a -->
        <input
            :value="user_income['11a']"
            class="formField z-30"
            style="top: 688px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 11b -->
        <input
            :value="user_income['11b']"
            class="formField z-30"
            style="top: 704px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 12a -->
        <input
            :value="user_income['12a']"
            class="formField z-30"
            style="top: 802px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 12b -->
        <input
            :value="user_income['12b']"
            class="formField z-30"
            style="top: 820px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 13a -->
        <input
            :value="user_income['13a']"
            class="formField z-30"
            style="top: 836px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 13b -->
        <input
            :value="user_income['13b']"
            class="formField z-30"
            style="top: 852px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 14 -->
        <input
            :value="user_income['14']"
            class="formField z-30"
            style="top: 870px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 15 -->
        <input
            :value="user_income['15']"
            class="formField z-30"
            style="top: 886px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 16 -->
        <input
            :value="user_income['16']"
            class="formField z-30"
            style="top: 903px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 17 -->
        <input
            :value="user_income['federal-income-tax-withheld']"
            class="formField z-30"
            style="top: 920px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />
        <!-- 18a -->
        <input
            :value="user_income['earned-income-credit']"
            class="formField z-30"
            style="top: 952px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <!-- 18b -->
        <input
            :value="0"
            class="formField z-30"
            style="top: 970px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <!-- 18c -->
        <input
            :value="0"
            class="formField z-30"
            style="top: 987px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <!-- 18d -->
        <input
            :value="user_income['18d']"
            class="formField z-30"
            style="top: 1003px; left: 574px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <!-- 18e -->
        <input
            :value="user_income['18e']"
            class="formField z-30"
            style="top: 1020px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <!-- 19 -->
        <input
            :value="user_income['19']"
            class="formField z-30"
            style="top: 1036px; left: 704px; width: 100px; height: 14px; font-size: 14px"
            disabled
        />

        <img
            class="absolute"
            src="../assets/1040combined.jpg"
            style="position:absolute; top:0; right:0;"
        />

        <!-- Filing Status -->
        <img
            v-if="filingStatus === 'SINGLE'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 134px;"
        />
        <img
            v-if="filingStatus === 'MFJ'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 194px;"
        />
        <img
            v-if="filingStatus === 'MFS'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 315px;"
        />
        <img
            v-if="filingStatus === 'HOH'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 476px;"
        />
        <img
            v-if="filingStatus === 'QW'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 616px;"
        />

        <!-- User Info -->
        <input
            class="absolute formField"
            v-model="user['given-name']"
            style="top: 155px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="user['last-name']"
            style="top: 155px; left: 336px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 221px; left: 584px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="user['street_address']"
            style="top: 221px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            :value="cityState"
            style="top: 255px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="socialSecurity"
            style="top: 155px; left: 658px;"
            size="50"
            disabled
        />
        <img
            v-if="campaignFund"
            class="check"
            src="../assets/check.png"
            style="top:259px; left: 717px;"
        />

        <!-- User Spouse Info -->
        <div v-if="filingStatus === 'MFJ'">
            <input
                class="formField"
                v-model="spouse['given-name']"
                style="top: 188px; left: 56px;"
                size="50"
                disabled
            />
            <input
                class="formField"
                v-model="spouse['last-name']"
                style="top: 188px; left: 336px;"
                size="50"
                disabled
            />
            <input
                class="formField"
                v-model="dummy"
                style="top: 188px; left: 658px;"
                size="50"
                disabled
            />
            <input
                class="formField"
                v-model="dummy"
                style="top: 188px; left: 696px;"
                size="50"
                disabled
            />
            <input
                class="formField"
                v-model="dummy"
                style="top: 188px; left: 728px;"
                size="50"
                disabled
            />
        </div>

        <!-- Foreign Country Info -->
        <input
            class="formField"
            v-model="dummy"
            style="top: 288px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 288px; left: 367px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 288px; left: 568px;"
            size="50"
            disabled
        />

        <!-- Standard Deduction/Blindess -->
        <img
            v-if="claimDependent === 'you'"
            class="check"
            src="../assets/check.png"
            style="top:310px; left: 234px;"
        />
        <img
            v-if="claimDependent === 'spouse'"
            class="check"
            src="../assets/check.png"
            style="top:310px; left: 365px;"
        />

        <img
            v-if="blindness.you.bornBefore"
            class="check"
            src="../assets/check.png"
            style="top:352px; left: 164px;"
        />
        <img
            v-if="user['blind']"
            class="check"
            src="../assets/check.png"
            style="top:352px; left: 345px;"
        />

        <img
            v-if="blindness.you.bornBefore"
            class="check"
            src="../assets/check.png"
            style="top:352px; left: 475px;"
        />
        <img
            v-if="spouse['spouse-blind']"
            class="check"
            src="../assets/check.png"
            style="top:352px; left: 656px;"
        />

        <!-- Dependent Info -->
        <img
            v-if="moreThan4"
            class="check"
            src="@/assets/check.png"
            style="top:292px; left: 793px;"
        />
        <DependentField
            class="absolute"
            v-for="(dep, index) in dependents"
            v-bind:key="index"
            :depIndex="index"
            :style="{ top: 401 + 15 * index + 'px' }"
            style="width:868px; left: 0px"
        />

        <!-- Money Info -->
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 469px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 485px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 502px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 519px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 536px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 553px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 570px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 586px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 603px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 620px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            v-model="dummyNum"
            class="formField"
            style="top: 636px; left: 708px; font-size: 14px"
            size="50"
            disabled
        />

        <!-- Don't touch this - this is a crucical hack -->
        <input class="hidden" v-model="dirtyBit" />
    </div>
</template>

<script>
import DependentField from "@/components/DependentField.vue";
import { mapState } from "vuex";

export default {
    name: "Form1040",
    components: {
        DependentField
    },
    computed: {
        filingStatus: function() {
            const db = this.dirtyBit; //hack
            if (this.user["filing_status"] === "qualifying widow") return "QW";
            else if (this.user["filing_status"] === "head of household")
                return "HOH";
            else if (this.user["filing_status"] === "married filing jointly")
                return "MFJ";
            else if (this.user["filing_status"] === "married filing separately")
                return "MFS";
            else return null;
        },
        cityState: function() {
            const db = this.dirtyBit; //hack
            const city = this.user["city"];
            const state = this.user["state"];
            const zip = this.user["zip-code"];

            if (city && state && zip) {
                return city + ", " + state + ", " + zip;
            }
            return "";
        },
        socialSecurity: function() {
            const db = this.dirtyBit; //hack
            if (!this.user["social_security"]) return "";
            let str = "";
            for (let i = 0; i < 9; i++) {
                str += this.user["social_security"][i] + " ";
            }
            str = str.slice(0, 5) + " " + str.slice(5, 9) + " " + str.slice(9);
            return str;
        },
        ...mapState({
            user: state => state.document.user,
            user_income: state => state.document.user_income,
            spouse: state => state.document.spouse,
            dependents: state => state.document.dependents,
            dirtyBit: state => state.document.dirtyBit
        })
    },
    data() {
        return {
            dummy: null,
            dummyNum: null,
            campaignFund: false,
            moreThan4: false,
            claimDependent: null, //"spouse",
            blindness: {
                you: {
                    bornBefore: false
                },
                spouse: {
                    bornBefore: false
                }
            },
            dependentCredit: {
                d1: {
                    child: false,
                    other: false
                },
                d2: {
                    child: false,
                    other: false
                },
                d3: {
                    child: false,
                    other: false
                },
                d4: {
                    child: false,
                    other: false
                }
            }
        };
    }
};
</script>

<style scoped>
.formField {
    position: absolute;
    background-color: rgba(0, 0, 0, 0);
    line-height: 3px;
    color: red;
}

.check {
    position: absolute;
    width: 15px;
}
</style>
