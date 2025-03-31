{{/*
Expand the name of the chart.
*/}}
{{- define "centridesk-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "centridesk-backend.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "centridesk-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "centridesk-backend.labels" -}}
helm.sh/chart: {{ include "centridesk-backend.chart" . }}
{{ include "centridesk-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "centridesk-backend.selectorLabels" -}}
{{- if .consumerName -}}
app.kubernetes.io/name: {{ printf "%s-%s" (include "centridesk-backend.name" .) .consumerName | trunc -63 }}
{{- else -}}
app.kubernetes.io/name: {{ include "centridesk-backend.name" . }}
{{- end }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "centridesk-backend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "centridesk-backend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
define livenessProbe
*/}}
{{- define "centridesk-backend.livenessProbe" -}}
            livenessProbe:
              httpGet:
                path: {{ .Values.livenessProbe.path | default .Values.probePath }}
                port: {{ .Values.service.internalPort }}
                scheme: HTTP
                httpHeaders:
                - name: Host
                  value: {{ include "centridesk-backend.fullname" . }}
              initialDelaySeconds: {{ .Values.livenessProbe.initialDelaySeconds }}
              periodSeconds: {{ .Values.livenessProbe.periodSeconds }}
              successThreshold: {{ .Values.livenessProbe.successThreshold }}
              timeoutSeconds: {{ .Values.livenessProbe.timeoutSeconds }}
{{- end -}}

{{/*
define redinessProbe
*/}}
{{- define "centridesk-backend.redinessProbe" -}}
            readinessProbe:
              failureThreshold: {{ .Values.readinessProbe.failureThreshold }}
              httpGet:
                path: {{ .Values.readinessProbe.path | default .Values.probePath }}
                port: {{ .Values.service.internalPort }}
                scheme: HTTP
                httpHeaders:
                - name: Host
                  value: {{ include "centridesk-backend.fullname" . }}
              initialDelaySeconds: {{ .Values.readinessProbe.initialDelaySeconds }}
              periodSeconds: {{ .Values.readinessProbe.periodSeconds }}
              successThreshold: {{ .Values.readinessProbe.successThreshold }}
              timeoutSeconds: {{ .Values.readinessProbe.timeoutSeconds }}
{{- end -}}

