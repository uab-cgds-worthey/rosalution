<template>
    <div class="discussion-post">
        <div class="discussion-header">
            <b>{{ author_name }}</b>
            {{  timestamp  }}
        </div>
        <div class="discussion-content">
            {{ content }}
        </div>
    </div>
</template>

<script>
export default {
    name: "discussion-post",
    props: {
        id: {
            type: String
        },
        author_id: {
            type: String
        },
        author_name: {
            type: String
        },
        publish_timestamp: {
            type: String
        },
        content: {
            type: String
        },
        attachments: {
            type: Array,
            default: () => {
                return [];
            },
        },
        thread: {
            type: Array,
            default: () => {
                return [];
            },
        },
    },
    computed: {
        timestamp: function() {
            return new Date(this.publish_timestamp).toUTCString()
        }
    }
}
</script>

<style scoped>
.discussion-post {
    background-color: var(--rosalution-grey-50);
    border-radius: var(--content-border-radius);
    padding: var(--p-8);
    margin: var(--p-8);
    
}

.discussion-header {
    margin-top: var(--p-5);
    margin-bottom: var(--p-5);
}

.discussion-content {
    margin-bottom: var(--p-10);
}

</style>