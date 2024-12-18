{{/* vim: set filetype=mustache: */}}

{{/*
Create the name of the service account to use
*/}}
{{- define "netbox-operator.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
  {{- default (include "common.names.fullname" .) .Values.serviceAccount.name | trunc 63 | trimSuffix "-" }}
{{- else }}
  {{- default "default" .Values.serviceAccount.name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Name of the Secret that contains the NetBox API Token
*/}}
{{- define "netbox-operator.netbox.secret" -}}
  {{- if .Values.netbox.enabled }}
    {{- printf "%s-%s" (include "common.names.dependency.fullname" (dict "chartName" "netbox" "chartValues" .Values.netbox "context" .)) "superuser" | trunc 63 | trimSuffix "-" }}
  {{- else }}
    {{- include "common.secrets.name" (dict "existingSecret" .Values.auth.existingSecret "defaultNameSuffix" "netbox-auth" "context" .) }}
  {{- end }}
{{- end }}
