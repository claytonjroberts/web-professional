

<template>
    <div class="col-auto border skill"
        @click="$parent.skilladditional = ($parent.skilladditional == skillkey ? null : skillkey)"
        @mouseover="showlink = true" @mouseleave="showlink = false">



        <div class="row justify-content-start">
            <div class="col-1 text-muted content-center-vertical-with-margin" style="min-width: 3em; text-align: center;">
                <div>
                    <span class="skill-icon" v-if="showIcon">
                        <i :class="skilldict.icon ? skilldict.icon : parentDict.icon" style="align-self:center;"></i>
                    </span>
                    <span class="skill-icon" v-if="showIconText">
                        {{ skilldict.icontext }}
                    </span>
                </div>

            </div>
            <div class="col content-center-vertical-with-margin">
                <h5 class="skill-name">{{ skillkey }}</h5>
                <h6 class="skill-name-parent text-muted" v-if="skilldict.parent">
                    {{ skilldict.parent }}
                </h6>
                <!-- {{ skilldict.keyword }}
                {{ skillkey }} <span v-if="skilldict.parent">(<span class="skill-text-parent">{{ skilldict["parent"]
                }}</span>)</span> -->
            </div>
            <div class="col-auto skill-experience">
                <div class="text-tertiary stars">
                    <i class="fas fa-star fa-xs" v-for="x in this.$_.range(Math.ceil(skilldict.level / 2))"
                        :key="`star-${x}`">
                    </i><i class="far fa-star fa-xs" v-for="x in this.$_.range(3 - Math.ceil(skilldict.level / 2))"
                        :key="`star-empty-${x}`">
                    </i>
                </div>
                <div>
                    <span class="skill-years" v-if="experience_years">
                        {{ experience_years }} yrs
                    </span>
                </div>
            </div>
        </div>
        <div class="row justify-content-start" v-if="skilldict.use">
            <div class="col-auto skill-description">
                {{ skilldict.use }}
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "skill",
    props: [
        "skilldict",
        "skillkey",
    ],
    data: function () {
        return {
            showadditional: false,
            showlink: false,
        }
    },
    computed: {
        doshow() {
            return true;
            // `this` points to the vm instance
            var self = this;

            if (this.$parent.filterexperience) {
                return (0 <= _.indexOf(this.$parent.filterexperience, self.skillkey))
            }
            // return true;
            else if (this.$parent.filtersearch) {
                return (self.skillkey.includes(self.$parent.filtersearch) || (self.skilldict.parent && self.skilldict.parent.includes(self.$parent.filtersearch)));
            } else {
                return true;
            }

        },
        showIcon() {
            return (
                this.skilldict.icon || (this.parentDict && this.parentDict.icon)
            )
        },
        showIconText() {
            return (
                !(this.showIcon) &&
                (
                    this.skilldict.icontext ||
                    (this.parentDict && this.parentDict.icon)
                )
            )
        },
        parentDict() {
            var self = this;

            if (self.skilldict.parent) {
                return this.$parent.info.skills.list[self.skilldict.parent];
            } else {
                return null;
            }
        },
        stars: function () {
            var self = this;

            return _.range(Math.ceil(this.skilldict.level / 2))
        },
        experience_years: function () {
            var self = this;

            if (self.skilldict.experience.years) {
                return self.skilldict.experience.years;
            } else if (self.skilldict.experience.start) {
                var ageDifMs = Date.now() - Date.parse(self.skilldict.experience.start);
                var ageDate = new Date(ageDifMs); // miliseconds from epoch
                return Math.abs(ageDate.getUTCFullYear() - 1970);
            }
            return null;
        }
    },
    methods: {
        from_markdown_to_html: function (x) {
            return mdconverter.makeHtml(x);
        },
        sort_experience: function (x) {

        }
    },
}
</script>
