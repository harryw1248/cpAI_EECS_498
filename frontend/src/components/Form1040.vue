<template>
    <div class="relative" style="width: 868px; height: 1476px">
        <img
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
            v-model="user['street-address']"
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
        <input
            class="formField"
            v-model="dummy"
            style="top: 188px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
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
            style="height: 15px; width:868px; top: 401px; left: 0px"
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
        <input class="hidden" v-model="dirtyBit"/>
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
      else if (this.user["filing_status"] === "head of household") return "HOH";
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