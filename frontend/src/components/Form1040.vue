<template>
    <div class="relative" style="width: 856px; height: 1476px">
        <img
            src="../assets/1040combined.jpg"
            style="position:absolute; top:0;"
        />

        <!-- Filing Status -->
        <img
            v-if="dummy === 'Single'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 134px;"
        />
        <img
            v-if="dummy === 'MFJ'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 194px;"
        />
        <img
            v-if="dummy === 'MFS'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 315px;"
        />
        <img
            v-if="dummy === 'HOH'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 476px;"
        />
        <img
            v-if="dummy === 'QW'"
            class="check"
            src="../assets/check.png"
            style="top:92px; left: 616px;"
        />

        <!-- User Info -->
        <input
            class="absolute formField"
            v-model="params['first-name']"
            style="top: 155px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="params['last-name']"
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
            v-model="params['street-address']"
            style="top: 221px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="cityState"
            style="top: 255px; left: 56px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="params['social_security']"
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
            v-if="blindness.you.blind"
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
            v-if="blindness.you.bornBefore"
            class="check"
            src="../assets/check.png"
            style="top:352px; left: 656px;"
        />


        <!-- Dependent Info -->
        <img
            v-if="moreThan4"
            class="check"
            src="../assets/check.png"
            style="top:292px; left: 793px;"
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 401px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />
        <img
            v-if="dependentCredit.d1.child"
            class="check"
            src="../assets/check.png"
            style="top: 402px; left: 633px;"
        />
        <img
            v-if="dependentCredit.d1.other"
            class="check"
            src="../assets/check.png"
            style="top: 402px; left: 744px;"
        />

        <input
            class="formField"
            style="top: 418px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 418px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 418px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 418px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 418px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 418px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />
        <img
            v-if="dependentCredit.d2.child"
            class="check"
            src="../assets/check.png"
            style="top: 419px; left: 633px;"
        />
        <img
            v-if="dependentCredit.d2.other"
            class="check"
            src="../assets/check.png"
            style="top: 419px; left: 744px;"
        />

        <input
            class="formField"
            style="top: 435px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 435px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 435px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 435px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 435px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 435px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />
        <img
            v-if="dependentCredit.d3.child"
            class="check"
            src="../assets/check.png"
            style="top: 436px; left: 633px;"
        />
        <img
            v-if="dependentCredit.d3.other"
            class="check"
            src="../assets/check.png"
            style="top: 436px; left: 744px;"
        />

        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 452px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />
        <img
            v-if="dependentCredit.d4.child"
            class="check"
            src="../assets/check.png"
            style="top: 453px; left: 633px;"
        />
        <img
            v-if="dependentCredit.d4.other"
            class="check"
            src="../assets/check.png"
            style="top: 453px; left: 744px;"
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
import { mapState } from "vuex";

export default {
  name: "Form1040",
  computed: {
    cityState: function() {
      const city = this.params["city"];
      const state = this.params["state"];
      if (city && state) {
        return city + " " + state;
      }
      if (city) {
        return city;
      }
      if (state) {
        return state;
      }
      return "";
    },
    ...mapState({
      params: state => state.formData,
      dirtyBit: state => state.dirtyBit
    })
  },
  created: function() {
    const fields = [
      "age",
      "capital-gains",
      "city",
      "given-name",
      "is-married",
      "last-name",
      "num_dependents",
      "occupation",
      "owns-business",
      "pensions-annuities",
      "social_security",
      "ss-benefits",
      "state",
      "street-address",
      "wages",
      "zip-code"
    ];
    const dummyObj = {};
    for (const field of fields) {
      dummyObj[field] = null;
    }
    this.$store.dispatch("updateForm1040", dummyObj);
  },
  data() {
    return {
      dummy: "Rishabh",
      dummyNum: 100,
      campaignFund: true,
      moreThan4: true,
      claimDependent: "spouse",
      blindness: {
        you: {
            bornBefore: true,
            blind: true,
        },
        spouse: {
            bornBefore: true,
            blind: true,
        }
      },
      dependentCredit: {
        d1: {
            child: true,
            other: true,
        },
        d2: {
            child: true,
            other: true,
        },
        d3: {
            child: true,
            other: true,
        },
        d4: {
            child: true,
            other: true,
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