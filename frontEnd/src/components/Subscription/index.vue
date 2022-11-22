<template>
    <div class="subscription-container">
        <div class="subscription-header">Subscription:</div>
        <div class="subscription-content">
            <div
                :class="['subscription-plan', { active: active === index }]"
                v-for="(plan, index) in plans"
                :key="plan.id"
                @click="selectPlan(index)"
            >
                <span>{{ plan.name }}</span>
                <span>{{ plan.price }}</span>
            </div>
        </div>
        <div class="subscription-footer">
            <button class="submit" @click="handlePurchase">Subscribe</button>
        </div>

        <v-alert
            class="notification"
            v-model="notification"
            color="green"
            dark
            transition="scale-transition"
            dismissible
        >
            Thank you for subscription. We value you as a preferred customer and
            look forward to future business with you.
        </v-alert>
    </div>
</template>

<script>
import { purchaseOffering } from "@/api_client.js";

export default {
    name: "Subscription",
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            active: 0,
            notification: false,
            plans: [
                { id: 1, name: "30 Days", price: "100 SAR" },
                { id: 2, name: "90 Days", price: "250 SAR" },
                { id: 3, name: "360 Days", price: "450 SAR" },
            ],
        };
    },
    methods: {
        selectPlan(index) {
            this.active = index;
        },
        handlePurchase() {
            const payload = {
                offering: this.id,
                price: "100",
                period: "90",
            };
            purchaseOffering(payload);
            this.notification = true;
        },
    },
};
</script>

<style scoped lang="scss">
.subscription-container {
    border-radius: 5px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.125490196078431);
    background-color: #ffffff;

    .notification {
        position: fixed;
        top: 10px;
        right: 10px;
    }

    .subscription-header {
        padding: 10px 20px;
        color: #737373;
    }

    .subscription-plan {
        background-color: #ffffff;
        color: #000000;
        padding: 10px 20px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #c7c7c7;

        &:last-child {
            border-bottom: none;
        }

        &.active {
            color: #ffffff;
            background-color: #7b7b7b;
        }
    }

    .subscription-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;

        .submit {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #333333;
            color: #ffffff;
            cursor: pointer;
            max-width: 120px;
            position: relative;
            border-radius: 4px;
            box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
            background-image: linear-gradient(to right, #2f6bff, #5e82f5);
            padding: 8px 16px;
        }
    }
}
</style>
